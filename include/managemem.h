#include <stdlib.h>
#include <stdio.h>
#ifndef _mem_mangament_h
#define _mem_mangament_h


void * new(size_t size);

void delete(void *p);

void showmem();

typedef struct _memnode {
    size_t size;
    struct _memnode * next;
    struct _memnode * prev;
}MNODE;

#endif
