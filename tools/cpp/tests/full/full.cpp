#include <string>
#include <stdint.h>
#include "../../include/schematic.h"
#include "../../include/place.h"
#include "../../include/pcb.h"
#include "../../include/coords.h"

int main(int argc, char** argv, char** env) {
   
   std::string path = argv[1]; 
   Schematic sch(path);
   sch.Print(); 
   Place p(sch, 1);       
   p.PrintList(); 
   Pcb pcb(&sch, true,std::string("/home/ashleyjr/RTL-to-PCB/tools/cpp/tests/full/log.txt"));  
   p.PrintGrid();   
   uint32_t n;
   uint32_t n_last = 0;
   uint32_t l;
   uint32_t l_last = 0;
   uint32_t t;
   printf("Routing:\n");
   for(uint32_t i=0;i<1;i++){ 
      printf("%d/100\n",i); 
      //p.Randomise(1);
      pcb.Route(&p);
      n = pcb.NumRouted();
      l = pcb.NumCopper();  
      t = pcb.NumNets();
      printf("nets=(%d/%d),length=%d",n,t,l);
      if(n < n_last){
         p.UndoRandomise();
         printf("\n");
      }else{
         if((n == n_last) && (l > l_last)){
            p.UndoRandomise();
         }else{          
            printf(" <- \n");
            l_last = l;
            n_last = n; 
         }
      } 
   }
   
   pcb.Print();  
   
   path = argv[2];
   pcb.Dump(path);
   path = argv[3];
   p.Dump(path);

   return 0;
}

