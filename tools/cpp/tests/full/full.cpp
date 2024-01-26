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
   Place place(sch);      
   place.PrintList();
   Pcb pcb(&sch, &place, false); 
   place.PrintGrid();
   pcb.Print();
   printf("%d/%d\n",pcb.NumRouted(),pcb.NumNets());
   printf("%d\n",pcb.NumCopper());
   return 0;
}

