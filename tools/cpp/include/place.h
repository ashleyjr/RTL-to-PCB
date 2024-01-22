#ifndef PLACE_H
#define PLACE_H

#include "coords.h"
#include "schematic.h"

typedef struct Placed { 
   Cell cell;
   Coord pos;
   bool decap;
} Placed;


class Place{
   public:
      Place(Schematic s);
      uint8_t GetSize(void);
      const std::vector<Placed> GetPlacedSrcs(void);
      const std::vector<Placed> GetPlacedSinksAC(const Placed src);
      const std::vector<Placed> GetPlacedSinksBQ(const Placed src);  
      void PrintList(void);
      void PrintGrid(void);
   private:
      uint8_t sqr;
      std::vector<Placed> places;
};
#endif
