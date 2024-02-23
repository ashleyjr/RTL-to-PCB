#ifndef PLACE_H
#define PLACE_H

#include <stdlib.h> 

#include "coords.h"
#include "schematic.h"

typedef struct Placed { 
   Cell cell;
   Coord pos;
   bool decap;
} Placed;


class Place{
   public:
      Place(Schematic s, uint32_t extra_decap);
      void Randomise(uint32_t pairs);
      void UndoRandomise(void);
      uint8_t GetSize(void);
      const std::vector<Coord> GetNonDecap(void);
      const std::vector<Placed> GetPlacedSrcs(void);
      const std::vector<Placed> GetPlacedSinksAD(const Placed src);
      const std::vector<Placed> GetPlacedSinksBC(const Placed src);  
      void Dump(std::string path);
      void PrintList(void);
      void PrintGrid(void);
   private:
      uint8_t sqr;
      std::vector<uint32_t> swap_a;
      std::vector<uint32_t> swap_b;
      std::vector<Placed> places;
      std::vector<Placed> undo_places;
};
#endif
