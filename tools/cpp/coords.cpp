#include <stdlib.h>
#include <stdint.h>
#include "include/coords.h"

bool operator==(const Coord& l, const Coord& r){
   return ((l.x == r.x) && (l.y == r.y)); 
}

bool operator!=(const Coord& l, const Coord& r){
   return ((l.x != r.x) || (l.y != r.y)); 
}

uint32_t Distance(const Coord& l, const Coord& r){
   return abs(l.x - r.x) + abs(l.y - r.y);
}
