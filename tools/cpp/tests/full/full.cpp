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
   Place p(sch, 0);       
   p.PrintList(); 
   Pcb pcb(&sch, false);  
   p.PrintGrid(); 
   pcb.Route(&p);   
   uint32_t r = pcb.NumRouted();
   uint32_t t = pcb.NumNets();
   printf("nets=(%d/%d)\n",r,t);

   if(t == r){
      r--;
   }
   uint32_t n;
   uint32_t n_last = 0;
   uint32_t l;
   uint32_t l_last = 0;
   printf("Routing:\n");
   for(uint32_t i=0;i<10;i++){ 
      printf("%d/100\n",i); 
      pcb.Route(&p);  
      n = pcb.NumRouted();
      l = pcb.NumCopper(); 
      float a; 
      if(n <= r){
         a = 1;
      }else {
         a = 1 - (((float)t - (float)n)/((float)t - (float)r));
      }
      p.Randomise(a); 
      if(n < n_last){
         p.UndoRandomise();
      }else{
         if((n == n_last) && (l > l_last)){
            p.UndoRandomise();
         }else{          
            printf("a=%f: nets=(%d/%d),length=%d\n",a,n,t,l);
            l_last = l;
            n_last = n; 
         }
      } 
   }
   pcb.Route(&p);
   pcb.Print();
   p.PrintGrid();

   path = argv[2];
   pcb.Dump(path);
   path = argv[3];
   p.Dump(path);

   return 0;
}

