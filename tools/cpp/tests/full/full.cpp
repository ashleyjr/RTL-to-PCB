#include <string>
#include <stdint.h>
#include "../../include/schematic.h"
#include "../../include/place.h"
#include "../../include/pcb.h"
#include "../../include/coords.h"

int main(int argc, char** argv, char** env) { 
   std::string path = argv[1]; 
   Schematic sch(path);
   //sch.Print(); 
   Place p(sch, 1);        
   Pcb pcb(&sch, true,std::string("/home/ashleyjr/RTL-to-PCB/tools/cpp/tests/full/log.txt"));    
   printf("Routing:\n");
   for(uint32_t i=0;i<1;i++){  
      //p.Randomise(100); 
      pcb.Route(&p);
      uint32_t s = sch.GetNumNets();
      uint32_t n = pcb.NumRouted();
      uint32_t l = pcb.NumCopper();  
      uint32_t t = pcb.NumNets();
      printf("nets=%d, seeks=%d/%d, length=%d\n",s,n,t,l); 
   }
   
   //pcb.Print();  

   path = argv[2];
   pcb.Dump(path);
   path = argv[3];
   p.Dump(path);

   return 0;
}

