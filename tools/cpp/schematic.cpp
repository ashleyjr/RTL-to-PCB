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
                   getline(net, line);
                   c.net_b_c = std::stoi(line);
                   getline(net, line);
                   c.net_a_d = std::stoi(line);
                   getline(net, line);
                   c.net_y_q = std::stoi(line);
                   break;     
         case 'I': c.type = CellType::IN;
                   getline(net, line);
                   c.net_a_d = std::stoi(line);
                   c.net_b_c = std::stoi(line);
                   c.net_y_q = std::stoi(line);
                   break;     
         case 'N': c.type = CellType::NOR; 
                   getline(net, line);
                   c.net_a_d = std::stoi(line);
                   getline(net, line);
                   c.net_b_c = std::stoi(line);
                   getline(net, line);
                   c.net_y_q = std::stoi(line); 
                   break;    
         case 'O': c.type = CellType::OUT; 
                   getline(net, line);
                   c.net_a_d = std::stoi(line);
                   c.net_b_c = std::stoi(line);
                   c.net_y_q = std::stoi(line);
                   break;     
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
               c.net_b_c,
               c.net_a_d,
               c.net_y_q,
               c.name.c_str()
            );
            break;
         case CellType::IN:  
            printf("IN  \t%d\t\t\t (%s)\n",
               c.net_a_d,
               c.name.c_str()
            );
            break;
         case CellType::NOR:
            printf("NOR\tA %d \tB %d\t Y %d\t (%s)\n",
               c.net_a_d,
               c.net_b_c,
               c.net_y_q,
               c.name.c_str()
            );
            break;
         case CellType::OUT: 
            printf("OUT \t%d\t\t\t (%s)\n",
               c.net_a_d,
               c.name.c_str()
            );
            break;
      }
   }
}

std::vector<Cell> Schematic::GetCells(void){
   return cells;
}

bool lt (uint32_t i, uint32_t j) { return (i<j); }

std::vector<uint32_t> Schematic::GetNets(void){
   std::vector<uint32_t> nets;
   for (auto const& c : cells) { 
      bool found = false;
      for (auto const& n : nets) {   
         if(n == c.net_a_d) found = true;
      }
      if(!found) nets.push_back(c.net_a_d); 
      found = false;
      for (auto const& n : nets) {   
         if(n == c.net_b_c) found = true;
      }
      if(!found) nets.push_back(c.net_b_c);
      found = false;
      for (auto const& n : nets) {   
         if(n == c.net_y_q) found = true;
      }
      if(!found) nets.push_back(c.net_y_q); 
   }
   std::sort(nets.begin(), nets.end(), lt);
   return nets;
}

uint32_t Schematic::GetNumNets(void){
   return GetNets().size();
}


