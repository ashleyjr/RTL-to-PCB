#ifndef CELL_H
#define CELL_H

enum class CellType { 
   DFF,
   NOR,
   PAD
}

struct {                
   CellType t;
   uint8_t x;
   uint8_t y;
} cell;

#endif
