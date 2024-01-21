#include <string>
#include <stdint.h>
#include "../../include/schematic.h"
#include "../../include/place.h"
#include "../../include/pcb.h"

int main(int argc, char** argv, char** env) {
 
   std::string path = argv[1]; 
   Schematic sch(path);
   Place place(sch);      
   Pcb pcb(place,false); 
   return 0;
}

