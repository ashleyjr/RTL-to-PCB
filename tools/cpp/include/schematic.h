#ifndef SCHEMATIC_H
#define SCHEMATIC_H

#include <vector>

enum class CellType { 
   DFF,
   IN,
   NOR,
   OUT
};

typedef struct Cell { 
   CellType type;
   std::string name;
   uint32_t net_a_d;
   uint32_t net_b_c;
   uint32_t net_y_q; 
} Cell;

class Schematic{
   public:
      Schematic(std::string path);
      void Print(void);
   private:
      std::vector<Cell> cells;
};

#endif
