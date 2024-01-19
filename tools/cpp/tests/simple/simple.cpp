#include <stdint.h>
#include "../../include/pcb.h"

int main(int argc, char** argv, char** env) {
     
   Pcb p(50,false);
   Coord c[10];

   c[0].x = 1; 
   c[0].y = 1; 
   c[1].x = 22; 
   c[1].y = 22; 
   p.AddTrace(c,2);
    
   c[0].x = 23; 
   c[0].y = 28; 
   c[1].x = 23; 
   c[1].y = 10;    
   p.AddTrace(c,2);

   c[0].x = 25; 
   c[0].y = 28; 
   c[1].x = 25; 
   c[1].y = 10;    
   p.AddTrace(c,2);
   
   c[0].x = 10; 
   c[0].y = 28; 
   c[1].x = 30; 
   c[1].y = 28;    
   p.AddTrace(c,2);

   c[0].x = 23; 
   c[0].y = 40; 
   c[1].x = 23; 
   c[1].y = 0;    
   p.AddTrace(c,2);

   p.Print();

   return 0;
}

