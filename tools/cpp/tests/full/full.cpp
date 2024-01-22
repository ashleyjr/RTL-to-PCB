#include <string>
#include <stdint.h>
#include "../../include/schematic.h"
#include "../../include/place.h"
#include "../../include/pcb.h"
#include "../../include/coords.h"

int main(int argc, char** argv, char** env) {
 
   std::string path = argv[1]; 
   Schematic sch(path);
   Place place(sch);      
   place.PrintList();
   Pcb pcb(&sch, &place, true); 
   pcb.Print();
   return 0;
}

