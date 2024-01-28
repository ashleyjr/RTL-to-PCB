#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <vector>
#include <cmath>
#include "include/schematic.h"   
#include "include/place.h"   

Place::Place(Schematic s, uint32_t extra_decap){      
   // Copy cells over from schematic
   for (auto const& c : s.GetCells()) {   
      Placed p;
      p.cell = c;
      p.decap = false;
      places.push_back(p);
   }
   // Find minimum square size
   sqr = std::ceil(sqrt(places.size()));
   sqr += extra_decap;
   // Square off with decap spaces
   for(uint32_t i=places.size();i<(sqr*sqr);i++){
      Placed p;
      p.decap = true;
      places.push_back(p);
   }
   // Assign positions
   uint32_t x = 0;
   uint32_t y = 0;
   for(uint32_t i=0;i<(sqr*sqr);i++){ 
      places[i].pos.x = x; 
      places[i].pos.y = y;
      x++;
      if(x == sqr){
         x = 0;
         y++;
      }
   }
}

void Place::Randomise(float pairs){   
   
   swap_a.clear();
   swap_b.clear();
   
   uint32_t swaps = (uint32_t)(pairs * ((sqr*sqr)/2)); 
   for(uint32_t i=0;i<swaps;i++){   
      swap_a.push_back(rand() % places.size()); 
      swap_b.push_back(rand() % places.size()); 
      Coord temp = places[swap_a[i]].pos;
      places[swap_a[i]].pos = places[swap_b[i]].pos;
      places[swap_b[i]].pos = temp;
   }
      
}

void Place::UndoRandomise(void){     
   for(uint32_t i=swap_a.size()-1;i>0;i--){   
      Coord temp = places[swap_a[i]].pos;
      places[swap_a[i]].pos = places[swap_b[i]].pos;
      places[swap_b[i]].pos = temp;
   }
      
}

uint8_t Place::GetSize(void){
   return sqr;
}

const std::vector<Coord> Place::GetNonDecap(void){
   std::vector<Coord> s;
   for (auto const& p : places) {   
      if(!p.decap){
         s.push_back(p.pos); 
      }
   }
   return s;
}

const std::vector<Placed> Place::GetPlacedSrcs(void){
   std::vector<Placed> s;
   for (auto const& p : places) {   
      if(!p.decap){
         if(p.cell.type != CellType::OUT){
            s.push_back(p);
         } 
      }
   }
   return s;
}

const std::vector<Placed> Place::GetPlacedSinksAC(const Placed src){
   std::vector<Placed> s;
   for (auto const& p : places) {   
      if(((p.cell.type ==  CellType::DFF) || 
          (p.cell.type ==  CellType::NOR) || 
          (p.cell.type ==  CellType::OUT)) &&  
          (src.cell.net_y_q == p.cell.net_a_c) && 
          (!p.decap)){
         s.push_back(p); 
      }
       
   }
   return s;
}

const std::vector<Placed> Place::GetPlacedSinksBQ(const Placed src){
   std::vector<Placed> s;
   for (auto const& p : places) {   
      if(((p.cell.type ==  CellType::DFF) || 
          (p.cell.type ==  CellType::NOR)) &&  
          (src.cell.net_y_q == p.cell.net_b_d) && 
          (!p.decap)){
         s.push_back(p); 
      }
       
   }
   return s;
}

void Place::PrintList(void){
   for (auto const& p : places) {   
      if(p.decap){
         printf("DECAP\t(%d,%d)\n", 
            p.pos.x,
            p.pos.y
         );
      }else{
         printf("%s\t(%d,%d)\n",
            p.cell.name.c_str(),
            p.pos.x,
            p.pos.y
         ); 
      }
   }
}


void Place::PrintGrid(void){
   for(uint8_t y=0;y<sqr;y++){ 
      for(uint8_t x=0;x<sqr;x++){
         for (auto const& p : places) {   
            if((p.pos.x == x) && (p.pos.y == y)){
               if(p.decap){
                  printf("DECAP\t");
               }else{
                  printf("%s\t",p.cell.name.c_str());
               }
            }
         }
      }
      printf("\n");
   }
}
