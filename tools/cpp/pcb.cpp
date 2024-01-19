#include <stdlib.h>
#include <stdint.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdio.h>
#include "include/pcb.h"
#include "include/coords.h"


bool operator==(const Path& l, const Path& r){
   return ((l.coord == r.coord) && (l.top_n_bottom == r.top_n_bottom)); 
}

Pcb::Pcb(uint32_t s, bool d){   
   debug = d;
   size = s;
   // Net number increments with every trace
   // Net 0 is empty
   net = 0;
   // Init layers
   for(uint32_t x=0;x<size;x++){
      for(uint32_t y=0;y<size;y++){
         top[x][y] = 0;
         via[x][y] = 0;
         bot[x][y] = 0;
         top_ko[x][y] = 0; 
         bot_ko[x][y] = 0;
      }
   }
   // Top keepout region
   for(uint32_t x=0;x<size;x++){
      for(uint32_t y=KO_TOP_OFFSET;y<size;y+=KO_TOP_PITCH){ 
         for(uint32_t w=0;w<KO_TOP_WIDTH;w++){ 
            top_ko[x][y+w] = 1;
         }
      }
   }
   // Bottom keepout region
   for(uint32_t x=KO_BOT_OFFSET;x<size;x+=KO_BOT_PITCH){
      for(uint32_t y=0;y<size;y++){ 
         for(uint32_t w=0;w<KO_BOT_WIDTH;w++){ 
            bot_ko[x+w][y] = 1;
         }
      }
   }
}

bool Pcb::KoFree(Path const p){
   if(p.top_n_bottom){
      return (top_ko[p.coord.x][p.coord.y] == 0);
   }else{
      return (bot_ko[p.coord.x][p.coord.y] == 0);
   }
}

bool Pcb::CopperOk(Path const p){
   if(p.top_n_bottom){
      return ((top[p.coord.x][p.coord.y] == 0) || (top[p.coord.x][p.coord.y] == net));
   }else{
      return ((bot[p.coord.x][p.coord.y] == 0) || (bot[p.coord.x][p.coord.y] == net));
   }
}

bool Pcb::In(Path const f, std::vector<Path> const l){
   return (std::find(l.begin(), l.end(), f) != l.end());
}

bool Pcb::AddTrace(Coord const c[], uint8_t const l){ 
   net++;
      
   // Must have a least two points
   if(l < 2){
      return false;
   }

   // Check all points on top copper are free 
   for(uint32_t i=0;i<l;i++){
      if((top[c[i].x][c[i].y] != 0) ||
         (top_ko[c[i].x][c[i].y] == 1)) {
         return false;  
      } 
   }

   // Route each pair
   // - TODO: Could change order of pairs for shorter
   //         distances
   for(uint32_t i=0;i<(l-1);i++){ 
      printf("Routing net %d, pair %d\n",net,i); 
      Coord s;
      Coord e; 
      s = c[i];
      e = c[i+1]; 
      std::vector<Path> avoid; 
      bool done = false;
      while(!done) {
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
                  t.coord.y--;
                  t.top_n_bottom = false;
                  if(KoFree(t) && CopperOk(t) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!e_edge){ 
                  Path t = path.back();
                  t.coord.x++;
                  if(KoFree(t) && CopperOk(t) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!s_edge){ 
                  Path t = path.back();
                  t.coord.y++;
                  t.top_n_bottom = false;
                  if(KoFree(t) && CopperOk(t) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!w_edge){ 
                  Path t = path.back();
                  t.coord.x--;
                  if(KoFree(t) && CopperOk(t) && !In(t, avoid) && !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
            }else{
               if(!n_edge){ 
                  Path t = path.back();
                  t.coord.y--;
                  if(KoFree(t) && CopperOk(t) && ! In(t, avoid)&& !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!e_edge){ 
                  Path t = path.back();
                  t.coord.x++;
                  t.top_n_bottom = true;
                  if(KoFree(t) && CopperOk(t) && ! In(t, avoid)&& !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!s_edge){ 
                  Path t = path.back();
                  t.coord.y++;
                  if(KoFree(t) && CopperOk(t) && ! In(t, avoid)&& !In(t, path)){ 
                     options.push_back(t);     
                  }
               }
               if(!w_edge){ 
                  Path t = path.back();
                  t.coord.x--;
                  t.top_n_bottom = true;
                  if(KoFree(t) && CopperOk(t) && ! In(t, avoid)&& !In(t, path)){ 
                     options.push_back(t);     
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
            std::vector<uint32_t> dists; 
            for (auto const& opt : options) {    
               dists.push_back(Distance(e,opt.coord)); 
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
   }
   
   return true;
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
         if(top[x][y] != 0)    code |= 0x01;
         if(bot[x][y] != 0)    code |= 0x02;
         if(via[x][y] != 0)    code |= 0x04;
         if(top_ko[x][y] != 0) code |= 0x08;
         if(bot_ko[x][y] != 0) code |= 0x10;
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
         }
      }
      printf("\n");
   }
}

