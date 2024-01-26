#include <stdlib.h>
#include <stdint.h>
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

Pcb::Pcb(Schematic * s, Place * p, bool d){   
   schematic = s;
   places = p;
   debug = d;
   size = (places->GetSize() * CELL_SIZE) + 4; 
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
      start.x *= CELL_SIZE;
      start.y *= CELL_SIZE;           
      start.x += 10;
      start.y += 9;
      for (auto const& sink : places->GetPlacedSinksAC(src)){     
         Seek s;
         s.start = start;
         s.end = sink.pos;
         s.end.x *= CELL_SIZE; 
         s.end.x += 6;
         s.end.y *= CELL_SIZE;
         s.end.y += 2;
         s.net = src.cell.net_y_q;
         seeks.push_back(s);
      }
      for (auto const& sink : places->GetPlacedSinksBQ(src)){    
         Seek s;
         s.start = start;
         s.end = sink.pos;
         s.end.x *= CELL_SIZE; 
         s.end.x += 6;
         s.end.y *= CELL_SIZE;
         s.end.y += 9;
         s.net = src.cell.net_y_q;
         seeks.push_back(s); 
      }
   }
   // Reserve start/ends
   for(auto const& seek  : seeks){
      top[seek.start.x][seek.start.y] = seek.net;
      top[seek.end.x][seek.end.y] = seek.net;
   } 
   // Top keepout region
   for(uint32_t x=0;x<size;x++){
      for(uint32_t y=KO_TOP_OFFSET;y<size;y+=KO_TOP_PITCH){ 
         for(uint32_t w=0;w<KO_TOP_WIDTH;w++){ 
            top_ko[x][y+w] = 1;
         }
      }
   }
   //// Bottom keepout region
   for(uint32_t x=KO_BOT_ODD_OFFSET;x<size;x+=KO_BOT_ODD_PITCH){
      for(uint32_t y=0;y<size;y++){ 
         for(uint32_t w=0;w<KO_BOT_ODD_WIDTH;w++){ 
            bot_ko[x+w][y] = 1;
         }
      }
   }
   for(uint32_t x=KO_BOT_EVEN_OFFSET;x<size;x+=KO_BOT_EVEN_PITCH){
      for(uint32_t y=0;y<size;y++){ 
         for(uint32_t w=0;w<KO_BOT_EVEN_WIDTH;w++){ 
            bot_ko[x+w][y] = 1;
         }
      }
   }
   // Route
   for(auto const& seek  : seeks){
      bool ok;
      ok = AddTrace(seek.start,seek.end,seek.net);
      oks.push_back(ok);
   }
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

bool Pcb::AddTrace(Coord const start, Coord const end, int32_t const net){ 
   // Route each pair
   // - TODO: Could change order of pairs for shorter
   //         distances 
   printf("Routing net %d Start (%d,%d) End (%d,%d)\n",
      net,
      start.x,
      start.y,
      end.x,
      end.y
   ); 
   Coord s;
   Coord e; 
   s = start;
   e = end; 
   std::vector<Path> avoid; 
   bool done = false;
   for(uint32_t t=0;t<100;t++) {
      std::vector<Path> path; 
      path.push_back({.coord = s, .top_n_bottom = true});
      while (!done) { 
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
        
         // Print the route
         if(debug){
            printf("(%d,%d),",path.back().coord.x,path.back().coord.y);
            for (auto const& opt : options) {   
               printf("(%d,%d),",opt.coord.x,opt.coord.y);
            }
            printf("\n");
         }

         // If nowhere to go
         if(options.size() == 0){
            if(debug){
               printf("Failed to route");
            }
            avoid.push_back(path.back());
            break;
         } 

         // Find the distance from each option
         // - Add 1 for each via
         std::vector<uint32_t> dists; 
         for (auto const& opt : options) {    
            uint32_t d = Distance(e,opt.coord);
            if(path.back().top_n_bottom != opt.top_n_bottom){
               d++;
            }
            dists.push_back(d); 
         }          
         std::vector<uint32_t>::iterator m = std::min_element(dists.begin(), dists.end()); 
         Path p = options[std::distance(dists.begin(), m)]; 
         if(path.back().top_n_bottom != p.top_n_bottom) { 
            Path v = path.back();
            v.top_n_bottom = p.top_n_bottom;
            path.push_back(v);
         }
         path.push_back(p);
         
         // Special case if there but on the wrong side
         if((path.back().coord == e) && (path.back().top_n_bottom == false)){
            Path s;
            s.coord = path.back().coord;
            s.top_n_bottom = true;
            path.push_back(s);
         }

         done = (path.back().coord == e) && (path.back().top_n_bottom == true);  
      }
      // Update the copper
      if(done){
         Path last;
         last.coord.x = 0;
         last.coord.y = 0;
         last.top_n_bottom = true;  
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
   for (auto const& ok : oks){    
      if(ok) i++;
   }
   return i;
}

uint32_t Pcb::NumNets(void){
   uint32_t i=0;
   for (auto const& ok : oks){    
      i++;
   }
   return i;
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

