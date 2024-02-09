#ifndef COORDS_H
#define COORDS_H

typedef struct Coord{                
   uint8_t x;
   uint8_t y;
} Coord;

bool operator!=(const Coord& l, const Coord& r);
bool operator==(const Coord& l, const Coord& r);
float Euclidean(const Coord& s, const Coord& e);
uint32_t Manhattan(const Coord& s, const Coord& e);

#endif
