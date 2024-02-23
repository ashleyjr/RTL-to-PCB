#include <stdlib.h>
#include <stdint.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include "include/pcb.h"
#include "include/coords.h"
#include "include/place.h"



bool operator==(const Path& l, const Path& r){
   return ((l.coord == r.coord) && (l.top_n_bottom == r.top_n_bottom)); 
}

Pcb::Pcb(Schematic * s, bool d, std::string p){   
   schematic = s;
   debug = d;
   if(debug){
      debug_file.open(p);
   }
}

Pcb::~Pcb(void){
   debug_file.close();
}
  
void Pcb::Init(){
   // Init layers
   for(uint32_t x=0;x<size;x++){
      for(uint32_t y=0;y<size;y++){
         top[x][y] = -1;
         via[x][y] = -1;
         bot[x][y] = -1;
         top_ko[x][y] = -1; 
         bot_ko[x][y] = -1;
      }
   }
   // Create start and ends to seek
   for (auto const& src : places->GetPlacedSrcs()){    
      Coord start = src.pos;
      start.x *= CELL_SCALE_X;
      start.y *= CELL_SCALE_Y;           
      start.x += 6;
      start.y += 11;
      for (auto const& sink : places->GetPlacedSinksAD(src)){     
         Seek s;
         s.start = start;
         s.end = sink.pos;
         s.end.x *= CELL_SCALE_X; 
         s.end.x += 3;
         s.end.y *= CELL_SCALE_Y;
         s.end.y += 4;
         s.net = src.cell.net_y_q;
         seeks.push_back(s);
      }
      for (auto const& sink : places->GetPlacedSinksBC(src)){    
         Seek s;
         s.start = start;
         s.end = sink.pos;
         s.end.x *= CELL_SCALE_X; 
         s.end.x += 6;
         s.end.y *= CELL_SCALE_Y;
         s.end.y += 4;
         s.net = src.cell.net_y_q;
         seeks.push_back(s); 
      }
   }
   // Reserve start/ends
   for(auto const& seek  : seeks){
      bot[seek.start.x][seek.start.y] = seek.net;
      bot[seek.end.x][seek.end.y] = seek.net;
   } 
   // Top keepout region are horizontal strips
   for(uint32_t x=0;x<size;x++){
      for(uint32_t y=KO_TOP_OFFSET;y<size;y+=KO_TOP_PITCH){ 
         for(uint32_t w=0;w<KO_TOP_WIDTH;w++){ 
            top_ko[x][y+w] = 1;
         }
      }
   }
   // Bottom keepout region appear under all but DECAP cells
   for (auto const& c : places->GetNonDecap()) {   
      Coord start;
      Coord end;
      start.x = (c.x * CELL_SCALE_X) + KO_BOT_OFFSET ;
      start.y = (c.y * CELL_SCALE_Y) + KO_TOP_OFFSET;
      end.x = start.x + KO_BOT_WIDTH;
      end.y = start.y + KO_TOP_WIDTH; 
      for(uint32_t x=start.x;x<end.x;x++){
         for(uint32_t y=start.y;y<end.y;y++){
            bot_ko[x][y] = 1;
         }
      }
   }
}
void Pcb::Route(Place * p){   
   places = p;
   seeks.clear(); 
   size = (places->GetSize() * PCB_SCALE); 
   Init();  
   Mst();
   // Sort the seek distances
   std::vector<Seek> temp;
   uint32_t stop = seeks.size();
   for(uint32_t i=0;i<stop;i++){
      uint32_t min_idx = 0;
      uint32_t min = Manhattan(seeks[0].start,seeks[0].end);
      for(uint32_t j=1;j<seeks.size();j++){
         if(Manhattan(seeks[j].start,seeks[j].end) < min){
            min_idx = j;
            min = Manhattan(seeks[j].start,seeks[j].end);
         }
      }
      temp.push_back(seeks[min_idx]);
      seeks.erase(seeks.begin() + min_idx);
   }
   seeks = temp;

   
   // Route
   // - If a path cannot be routed, try them all again but pu hard one first
   //bool done = false;
   //while(!done){
   //   done = true;
      oks.clear();
      for(uint32_t i=0;i<seeks.size();i++){
         bool ok;
         ok = AddTrace(seeks[i].start,seeks[i].end,seeks[i].net);
         oks.push_back(ok);
         //if(!ok){
         //   Seek hard;
         //   hard = seeks[i];
         //   seeks.erase(seeks.begin() + i);
         //   seeks.insert(seeks.begin(), hard); 
         //   done = false;
         //   printf("nets=(%d/%d)\n",NumRouted(),NumNets());
         //   oks.clear();
         //   printf("%d\n",i);
         //   Init();
         //   break;
         //}
      }
   //}
}

bool Pcb::KoFree(Path const p){
   if(p.top_n_bottom){
      return (top_ko[p.coord.x][p.coord.y] == -1);
   }else{
      return (bot_ko[p.coord.x][p.coord.y] == -1);
   }
}

bool Pcb::CopperOk(Path const p, int32_t net){
   if(p.top_n_bottom){
      return ((top[p.coord.x][p.coord.y] == -1) || (top[p.coord.x][p.coord.y] == net));
   }else{
      return ((bot[p.coord.x][p.coord.y] == -1) || (bot[p.coord.x][p.coord.y] == net));
   }
}

bool Pcb::In(Path const f, std::vector<Path> const l){
   return (std::find(l.begin(), l.end(), f) != l.end());
}


bool lt_dist (Seek i, Seek j) { return (i.dist<j.dist); }

// Turns the seeks in to a Minimum Spanning Tree
void Pcb::Mst(){ 
   std::vector<Seek> mst;
 
   // Create a per net group MST
   for (auto const net : schematic->GetNets()){       
      
      // Create a list of nodes in a net group
      std::vector<Coord> nodes;
      for (auto const seek : seeks){   
         if(seek.net == net){
            bool found_start = false;
            bool found_end   = false;
            for (auto const n : nodes){
               if((seek.start.x == n.x) && (seek.start.y == n.y)) found_start = true;
               if((seek.end.x == n.x)   && (seek.end.y == n.y))   found_end  = true;
            }
            if(!found_start)  nodes.push_back(seek.start);
            if(!found_end)    nodes.push_back(seek.end);
         }
      }
     
      // List of all possible vertices with distances
      std::vector<Seek> net_seeks;
      for(uint32_t a=0;a<nodes.size();a++){
         for(uint32_t b=0;b<a;b++){ 
            Seek seek;
            seek.start = nodes[a];
            seek.end = nodes[b];
            seek.net = net;
            seek.dist = Manhattan(nodes[a],nodes[b]);
            net_seeks.push_back(seek);
         }
      }
 
      // Sort vertices in order of distance 
      std::sort(net_seeks.begin(), net_seeks.end(), lt_dist);

      // Find shortest vertices that do not create a loop 
      std::vector<Seek> net_mst;
      for(uint32_t i=0;i<net_seeks.size();i++){ 
         // Check for loop 
         bool loop = false; 
         net_mst.push_back(net_seeks[i]);
         // Testing must consider every node a route node once 
         for (auto const n : nodes){ 
            // Create a list of nodes not visited
            std::vector<Search> searches;
            for (auto const j : nodes){ 
               Search s;
               s.node = j;
               s.found = false;
               searches.push_back(s);
            }        
            // Test all edges
            std::vector<Seek> tests = net_mst;
            Coord ptr = n;
            bool back_to_root = true;
            bool done = false;
            while(!done){ 
               // Mark node as found 
               for(uint32_t j=0;j<searches.size();j++){
                  if(ptr == searches[j].node){
                     searches[j].found = true;
                     break;
                  }
               }
               // Find an edge to take 
               // - If two back to roots happens then done even if unvisited nodes
               bool found = false;
               uint32_t rm;
               for(rm=0;rm<tests.size();rm++){
                  if(tests[rm].start == ptr){  
                     found = true;
                     ptr = tests[rm].end;
                     break;
                  }   
                  if(tests[rm].end == ptr){
                     found = true; 
                     ptr = tests[rm].start;
                     break;
                  }
               }
               if(!found){
                  if(back_to_root){
                     done = true;
                  }else{
                     back_to_root = true;
                     ptr = n;
                  }
               }else{
                  back_to_root = false;
                  // Check node not already found (loop)
                  tests.erase(tests.begin() + rm);  
                  for(uint32_t j=0;j<searches.size();j++){
                     if((ptr == searches[j].node) && (searches[j].found == true)){ 
                        loop = true;
                        done = true;
                     }
                  }
               }
               if(tests.size() == 0){
                  done = true;
               }
            }
            if(loop){
               break;
            }
         }
         if(loop){
            net_mst.pop_back();
         }
      }

      uint32_t a = 0;
      uint32_t b = 0;

      for (auto const n : seeks){ 
         if(n.net == net){
            a++;
            //printf("seek: (%d,%d) - (%d,%d)\n",
            //n.start.x,
            //n.start.y,
            //n.end.x,
               //n.end.y
            //);
         }
      }  
      for (auto const n : net_seeks){ 
            if(n.net == net){
               //printf("net_seek: (%d,%d) - (%d,%d)  [%d]\n",
               //   n.start.x,
               //   n.start.y,
               //   n.end.x,
               //   n.end.y,
               //   n.dist
               //);
            }
         }


      for (auto const n : net_mst){ 
         if(n.net == net){
            b++;
            //printf("net_mst: (%d,%d) - (%d,%d)\n",
            //n.start.x,
            //n.start.y,
            //n.end.x,
            //n.end.y
            //);
         }
      }

      if(a != b){
         printf("fail\n");
      }

      for (auto const seek : net_mst){  
         mst.push_back(seek); 
      }
   }
   seeks.clear(); 
   seeks = mst;
}

bool Pcb::AddTrace(Coord const start, Coord const end, int32_t const net){  
   Coord s;
   Coord e; 
   s = start;
   e = end; 
   std::vector<Path> avoid; 
   bool done = false;
   for(uint32_t t=0;t<100;t++) {
      std::vector<Path> path; 
      path.push_back({.coord = s, .top_n_bottom = false});
      while (!done) { 
         // Debug the route
         if(debug){
            std::string add;
            if(path.back().top_n_bottom){
               add += "+t(";
            }else{
               add += "+b(";
            }
            add += std::to_string(path.back().coord.x);
            add += ",";
            add += std::to_string(path.back().coord.y);
            add += ")[";
            add += std::to_string(net);
            add += "]\n";
            debug_file << add;
         }

         std::vector<Path> options;
         bool n_edge = (path.back().coord.y) == 0;
         bool e_edge = (path.back().coord.x) == size-1;
         bool s_edge = (path.back().coord.y) == size-1;
         bool w_edge = (path.back().coord.x) == 0;
         if(path.back().top_n_bottom){
            if(!n_edge){ 
               Path t = path.back();
               t.top_n_bottom = false;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                  t.coord.y--;
                  if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
            }
            if(!e_edge){ 
               Path t = path.back();
               t.coord.x++;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                  options.push_back(t);     
               }
            }
            if(!s_edge){ 
               Path t = path.back();
               t.top_n_bottom = false;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){  
                  t.coord.y++;
                  if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
            }
            if(!w_edge){ 
               Path t = path.back();
               t.coord.x--;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                  options.push_back(t);     
               }
            }
         }else{
            if(!n_edge){ 
               Path t = path.back();
               t.coord.y--;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid)&& !In(t, path)){ 
                  options.push_back(t);     
               }
            }
            if(!e_edge){ 
               Path t = path.back();
               t.top_n_bottom = true;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                  t.coord.x++; 
                  if(KoFree(t) && CopperOk(t,net) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
            }
            if(!s_edge){ 
               Path t = path.back();
               t.coord.y++;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid)&& !In(t, path)){ 
                  options.push_back(t);     
               }
            }
            if(!w_edge){ 
               Path t = path.back();
               t.top_n_bottom = true;
               if(KoFree(t) && CopperOk(t,net) && !In(t, avoid)&& !In(t, path)){ 
                  t.coord.x--;
                  if(KoFree(t) && CopperOk(t,net) && !In(t, avoid)&& !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
            }
         }  

         // If nowhere to go
         if(options.size() == 0){
            if(debug){
               for (auto const p : path){    
                  std::string add;
                  if(p.top_n_bottom){
                     add += "-t(";
                  }else{
                     add += "-b(";
                  }
                  add += std::to_string(p.coord.x);
                  add += ",";
                  add += std::to_string(p.coord.y);
                  add += ")[";
                  add += std::to_string(net);
                  add += "]\n";
                  debug_file << add;
               }
            }
            avoid.push_back(path.back());
            break;
         } 

         // Find the distance from each option
         // - Add 1 for each via
         std::vector<float> dists; 
         for (auto const& opt : options) {    
            uint32_t d = Manhattan(e,opt.coord);
            if(path.back().top_n_bottom != opt.top_n_bottom){
               d++;
            }
            dists.push_back(d); 
         }          
         std::vector<float>::iterator m = std::min_element(dists.begin(), dists.end()); 
         Path p = options[std::distance(dists.begin(), m)]; 
         if(path.back().top_n_bottom != p.top_n_bottom) { 
            Path v = path.back();
            v.top_n_bottom = p.top_n_bottom;
            path.push_back(v);
         }
         path.push_back(p);
         
         // Special case if there but on the wrong side
         if((path.back().coord == e) && (path.back().top_n_bottom == true)){
            Path s;
            s.coord = path.back().coord;
            s.top_n_bottom = false;
            path.push_back(s);
         }

         done = (path.back().coord == e) && (path.back().top_n_bottom == false);  
      }
      // Update the copper
      if(done){
         Path last;
         last.coord.x = 0;
         last.coord.y = 0;
         last.top_n_bottom = false;  
         for (auto const& p : path) {   
            if(p.top_n_bottom != last.top_n_bottom){
               via[last.coord.x][last.coord.y] = 1; 
            }
            if(p.top_n_bottom){
               top[p.coord.x][p.coord.y] = net;
            }else{
               bot[p.coord.x][p.coord.y] = net;
            }
            last = p;
         }
      }
   }
   return done;
}

uint32_t Pcb::NumRouted(void){
   uint32_t i=0;
   for (auto  ok : oks){    
      if(ok) i++;
   }
   return i;
}

uint32_t Pcb::NumNets(void){ 
   return seeks.size();
}

uint32_t Pcb::NumCopper(void){
   uint32_t cnt=0;
   for(uint32_t i=0;i<size;i++){
      for(uint32_t j=0;j<size;j++){
         if(top[i][j] != -1){
            cnt++;
         }
         if(bot[i][j] != -1){
            cnt++;
         }
      }
   }
   return cnt;
}

void Pcb::Ripup(uint32_t net){
   for(uint32_t i=0;i<MAX_SIZE;i++){
      for(uint32_t j=0;j<MAX_SIZE;j++){
         if(top[i][j] == net){
            top[i][j] = 0;
         };
         if(via[i][j] == net){
            via[i][j] = 0;
         };
         if(bot[i][j] == net){
            bot[i][j] = 0;
         };;
      }
   }
}

void Pcb::Dump(std::string path){ 
   std::ofstream File(path);
   for(uint32_t y=0;y<size;y++){
      std::string xline = "";
      for(uint32_t x=0;x<size;x++){ 
         xline += std::to_string(top[x][y]);
         xline += ":";
         xline += std::to_string(via[x][y]);
         xline += ":";
         xline += std::to_string(bot[x][y]); 
         if(x != (size-1)){
            xline += ",";
         }
      }
      if(y != (size-1)){
         xline += "\n";
      }
      File << xline;
   }
   File.close();
}

void Pcb::Print(void){ 
   for(uint32_t y=0;y<size;y++){
      for(uint32_t x=0;x<size;x++){ 
         uint8_t code = 0;
         if(top[x][y] != -1)    code |= 0x01;
         if(bot[x][y] != -1)    code |= 0x02;
         if(via[x][y] != -1)    code |= 0x04;
         if(top_ko[x][y] != -1) code |= 0x08;
         if(bot_ko[x][y] != -1) code |= 0x10;
         for (auto const& seek : seeks){    
            if((seek.start.x == x) && 
               (seek.start.y == y)){
               code = 0x20;
            }
            if((seek.end.x == x) && 
               (seek.end.y == y)){
               code = 0x40;
            }
         }
         switch(code){
            case 0x00: printf("."); break;
            case 0x01: 
            case 0x11: printf("-"); break;
            case 0x02: 
            case 0x0A: printf("|"); break;
            case 0x03: printf("+"); break;
            case 0x04:
            case 0x05:
            case 0x06:
            case 0x07: printf("X"); break;
            case 0x08: printf(">"); break;
            case 0x10: printf("^"); break; 
            case 0x18: printf("#"); break;
            case 0x20: printf("S"); break; 
            case 0x40: printf("E"); break;
            // These should all be impossible
            case 0x09:
            case 0x0e:
            case 0x0f:
            case 0x12:
            case 0x13:
            case 0x17:
            case 0x1A: printf("?"); break; 
            // Catcg bad codes
            default:   printf("\n0x%x\n", code); break;
         } 
      }
      printf("\n");
   }
}

