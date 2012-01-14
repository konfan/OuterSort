#include <stdio.h>
#include "managemem.h"


//make a file struct

typedef struct fileslice_map {
    unsigned long minIndex;
    unsigned long maxIndex;
    char filename[8];
}FMAP;

extern FMAP * gMap;

#define BLOCK 1024
#define S_10M (1024*1024*10)


