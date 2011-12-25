#include "managemem.h"


static MNODE *head;
static MNODE *curNode;
static void init_mem()
{
    if( head == NULL ) {
        head = (MNODE *)calloc(1,sizeof(MNODE));
        if( head != NULL ) {
            head->next = NULL;
            head->size = sizeof(MNODE);
            curNode = head;
        }
    }
}


void * new(size_t size)
{
    init_mem();
    MNODE * cur = curNode;
    void * mem = calloc(1,size+sizeof(MNODE));
    MNODE * newnode = (MNODE *)mem;
    if( mem != NULL ) {
        cur->next = mem;
        newnode->size = size;
        newnode->next = NULL;
        curNode = newnode;
        return mem + sizeof(MNODE);
    }
    return NULL;
}

void delete(void *p)
{
    MNODE *start = head;
    while( start->next != NULL) {
        if( (void *)start + sizeof(MNODE) == p) {
            free( start );
        }
        start = start->next;
    }
}
