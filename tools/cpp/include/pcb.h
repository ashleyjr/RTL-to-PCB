#ifndef PCB_H
#define PCB_H

#include <vector>
#include "coords.h"
#include "place.h"

#define MAX_SIZE 100

#define CELL_SIZE 10

#define KO_TOP_OFFSET 5
#define KO_TOP_PITCH  10
#define KO_TOP_WIDTH  4

#define KO_BOT_OFFSET 5
#define KO_BOT_PITCH  10
#define KO_BOT_WIDTH  4

enum PinIn { 
   A, // NOR.A
   B, // NOR.B
   C, // DFF.CLK
   D, // DFF.DATA
   X  // PAD
};

enum PinOut { 
   Q, // DFF.OUTPUT 
   Y, // NOR.OUTPUT
   Z  // PAD
};


typedef struct Input{                  
   PinIn pin;
} Input;


typedef struct Fanout{                 
   PinOut out;
   std::vector<PinIn> fan;
} Fanout;


typedef struct Path{                
   Coord coord;
   bool top_n_bottom;
} Path;

bool operator==(const Path& l, const Path& r);

class Pcb{
   public:
      /*   size: The number of cells on the PCB
       */
      Pcb(Schematic * s, Place * p, bool d);
      /*   c: Array of coordinates
       *   l: Number of points in array
       */
      bool AddTrace(Coord const start, Coord const end, int32_t const net);
      void Print(void); 
   private: 
      uint32_t Route(Coord const s, Coord const e);
      void Ripup(uint32_t const net);
      bool KoFree(Path const p);
      bool CopperOk(Path const p, int32_t net);
      bool In(Path const f, std::vector<Path> const l); 
      Schematic * schematic;
      Place * places;
      bool debug;
      uint32_t size;
      int32_t top[MAX_SIZE][MAX_SIZE];  
      int32_t via[MAX_SIZE][MAX_SIZE];  
      int32_t bot[MAX_SIZE][MAX_SIZE];  
      int8_t top_ko[MAX_SIZE][MAX_SIZE];   
      int8_t bot_ko[MAX_SIZE][MAX_SIZE];  
};
#endif
