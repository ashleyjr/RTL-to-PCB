#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <vector>
#include <cmath>
#include "include/schematic.h"   
#include "include/place.h"   

Place::Place(Schematic s){      
   // Copy cells over from schematic
   for (auto const& c : s.GetCells()) {   
      Placed p;
      p.cell = c;
      p.decap = false;
      places.push_back(p);
   }
   // Find minimum square size
   sqr = std::ceil(sqrt(places.size()));
   // Square off with decap spaces
   for(uint32_t i=places.size();i<(sqr*sqr);i++){
      Placed p;
      p.decap = true;
      places.push_back(p);
   }
   // Assign positions
   for(uint8_t x=0;x<sqr;x++){
      uint16_t i = x * sqr;
      for(uint8_t y=0;y<sqr;y++){
         uint16_t j = 
         places[i+y].pos.x = x;
         places[i+y].pos.y = y;
      }
   }
}

uint8_t Place::GetSize(void){
   return sqr;
}

const std::vector<Placed> Place::GetPlacedSrcs(void){
   std::vector<Placed> s;
   for (auto const& p : places) {   
      if(p.cell.type != CellType::OUT){
         s.push_back(p);
      } 
   }
   return s;
}

const std::vector<Placed> Place::GetPlacedSinksAC(const Placed src){
   std::vector<Placed> s;
   for (auto const& p : places) {   
      if(((p.cell.type ==  CellType::DFF) || 
          (p.cell.type ==  CellType::NOR)) &&  
          (src.cell.net_y_q == p.cell.net_a_c)){
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
          (src.cell.net_y_q == p.cell.net_b_d)){
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
   for(uint8_t x=0;x<sqr;x++){ 
      for(uint8_t y=0;y<sqr;y++){
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
