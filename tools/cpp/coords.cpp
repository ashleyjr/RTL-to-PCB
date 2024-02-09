#include <stdlib.h>
#include <stdint.h>
#include <cmath>
#include "include/coords.h"

bool operator==(const Coord& l, const Coord& r){
   return ((l.x == r.x) && (l.y == r.y)); 
}

bool operator!=(const Coord& l, const Coord& r){
   return ((l.x != r.x) || (l.y != r.y)); 
}

float Euclidean(const Coord& l, const Coord& r){
   uint32_t x = abs(l.x - r.x);
   uint32_t y = abs(l.y - r.y);
   return sqrt((x * x) + (y * y));
}

uint32_t Manhattan(const Coord& l, const Coord& r){
   return abs(l.x - r.x) + abs(l.y - r.y);
}
