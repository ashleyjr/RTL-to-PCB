#include <stdint.h>
#include "../../include/pcb.h"

int main(int argc, char** argv, char** env) {
     
   Pcb p(50,true);
   Coord c[10];

   c[0].x = 26; 
   c[0].y = 3; 
   c[1].x = 26; 
   c[1].y = 11; 
   p.AddTrace(c,2);
   
   c[0].x = 20; 
   c[0].y = 12; 
   c[1].x = 30; 
   c[1].y = 12; 
   p.AddTrace(c,2);
      
   p.Print();

   return 0;
}

