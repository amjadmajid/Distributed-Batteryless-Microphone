
#include "common.h"

uint32_t    squared         (int16_t x);

extern uint16_t i_nv, j_nv;

__nv int start          = 0;
__nv int end            = (SAMPLES/FRAMESIZE);
__nv int lower          = 0;
__nv int upper          = 0;
__nv int backwards      = 0;
__nv int above          = 0;
//__nv     uint32_t treshold;
//__nv     uint32_t upper_treshold;
__nv uint32_t sum       = 0;
