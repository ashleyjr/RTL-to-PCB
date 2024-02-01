#ifndef PCB_H
#define PCB_H

#include <vector>
#include "coords.h"
#include "place.h"

#define MAX_SIZE 200

#define PCB_SCALE 15
#define CELL_SCALE_X 15
#define CELL_SCALE_Y 15

#define KO_TOP_OFFSET 5
#define KO_TOP_PITCH  15
#define KO_TOP_WIDTH  6

#define KO_BOT_OFFSET 3
#define KO_BOT_PITCH  12
#define KO_BOT_WIDTH  4

typedef struct Seek{                
   Coord start;
   Coord end;
   uint32_t net;
} Seek;

typedef struct Path{                
   Coord coord;
   bool top_n_bottom;
} Path;

bool operator==(const Path& l, const Path& r);

class Pcb{
   public:
      /*   size: The number of cells on the PCB
       */
      Pcb(Schematic * s, bool d);
      void Route(Place * p);

      /*   c: Array of coordinates
       *   l: Number of points in array
       */
      bool AddTrace(Coord const start, Coord const end, int32_t const net);
      uint32_t NumRouted(void);
      uint32_t NumNets(void);
      uint32_t NumCopper(void);
      void Dump(std::string path);
      void Print(void); 
   private: 
      void Ripup(uint32_t const net);
      bool KoFree(Path const p);
      bool CopperOk(Path const p, int32_t net);
      bool In(Path const f, std::vector<Path> const l); 
      Schematic * schematic;
      Place * places;
      std::vector<Seek> seeks;
      std::vector<bool> oks;
      bool debug;
      uint32_t size;
      int32_t top[MAX_SIZE][MAX_SIZE];  
      int32_t via[MAX_SIZE][MAX_SIZE];  
      int32_t bot[MAX_SIZE][MAX_SIZE];  
      int32_t top_ko[MAX_SIZE][MAX_SIZE];   
      int32_t bot_ko[MAX_SIZE][MAX_SIZE];  
};
#endif
