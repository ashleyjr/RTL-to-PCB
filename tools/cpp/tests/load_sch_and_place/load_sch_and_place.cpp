#include <string>
#include <stdint.h>
#include "../../include/schematic.h"
#include "../../include/place.h"


int main(int argc, char** argv, char** env) {
 
   std::string path = argv[1]; 
   Schematic s(path);
   Place p(s);      
   p.PrintGrid();
   return 0;
}

