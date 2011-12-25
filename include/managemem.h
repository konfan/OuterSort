#include <stdlib.h>
#ifndef _mem_mangament_h
#define _mem_mangament_h


void * new(size_t size);

void delete(void *p);


typedef struct _memnode {
    size_t size;
    struct _memnode * next;
}MNODE;

#endif
