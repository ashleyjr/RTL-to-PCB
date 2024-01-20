#include <string>
#include <stdint.h>
#include "../../include/schematic.h"

int main(int argc, char** argv, char** env) {
 
   std::string path = argv[1]; 
   Schematic s(path);
   s.Print();      
   return 0;
}

