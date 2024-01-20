#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
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
         c.net_a_d = std::stoi(line);
         c.net_b_c = std::stoi(line);
         c.net_y_q = std::stoi(line);
      }else{
         getline(net, line);
         c.net_a_d = std::stoi(line);
         getline(net, line);
         c.net_b_c = std::stoi(line);
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
            printf("DFF\tD %d \tCLK %d\t Q %d\t (%s)\n",
               c.net_a_d,
               c.net_b_c,
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
   printf("DF");
}
