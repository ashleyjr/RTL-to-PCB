#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <algorithm>
#include "include/schematic.h"   

Schematic::Schematic(std::string path){     
   std::string line;
   std::ifstream net(path);
   while (getline(net, line)) { 
      Cell c;
      c.name = line; 
      switch(line[0]){
         case 'D': c.type = CellType::DFF;
                   break;     
         case 'I': c.type = CellType::IN;
                   break;     
         case 'N': c.type = CellType::NOR; 
                   break;    
         case 'O': c.type = CellType::OUT; 
                   break;     
      }
      if((c.type == CellType::IN) || (c.type == CellType::OUT)){
         getline(net, line);
         c.net_a_c = std::stoi(line);
         c.net_b_d = std::stoi(line);
         c.net_y_q = std::stoi(line);
      }else{
         getline(net, line);
         c.net_a_c = std::stoi(line);
         getline(net, line);
         c.net_b_d = std::stoi(line);
         getline(net, line);
         c.net_y_q = std::stoi(line);
      }
      cells.push_back(c);
   }
   net.close();
}

void Schematic::Print(void){
   for (auto const& c : cells) {   
      switch(c.type){
         case CellType::DFF: 
            printf("DFF\tCLK %d \tD %d\t Q %d\t (%s)\n",
               c.net_a_c,
               c.net_b_d,
               c.net_y_q,
               c.name.c_str()
            );
            break;
         case CellType::IN:  
            printf("IN  \t%d\t\t\t (%s)\n",
               c.net_a_c,
               c.name.c_str()
            );
            break;
         case CellType::NOR:
            printf("NOR\tA %d \tB %d\t Y %d\t (%s)\n",
               c.net_a_c,
               c.net_b_d,
               c.net_y_q,
               c.name.c_str()
            );
            break;
         case CellType::OUT: 
            printf("OUT \t%d\t\t\t (%s)\n",
               c.net_a_c,
               c.name.c_str()
            );
            break;
      }
   }
}

std::vector<Cell> Schematic::GetCells(void){
   return cells;
}

std::vector<uint32_t> Schematic::GetNets(void){
   std::vector<uint32_t> nets;
   for (auto const& c : cells){
      if(std::find(nets.begin(), nets.end(), c.net_a_c) == nets.end()){ 
         nets.push_back(c.net_a_c);
      }
      if(std::find(nets.begin(), nets.end(), c.net_b_d) == nets.end()){
         nets.push_back(c.net_b_d);
      }
      if(std::find(nets.begin(), nets.end(), c.net_y_q) == nets.end()){
         nets.push_back(c.net_y_q);
      }
   }
   return nets;
}


