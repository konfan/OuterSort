#include "managemem.h"


static MNODE *head = NULL;
static MNODE *curNode;
static void init_mem()
{
    if( head == NULL ) {
        head = (MNODE *)calloc(1,sizeof(MNODE));
        if( head != NULL ) {
            head->prev = NULL;
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
        newnode->prev = cur;
        curNode = newnode;
        return mem + sizeof(MNODE);
    }
    return NULL;
}

void delete(void *p)
{
    MNODE *point = p - sizeof(MNODE);
    if( p == NULL || point == head)
        return;
    if( curNode == point) {
        curNode = curNode->prev;
        free(curNode->next);
        return;
    }
    MNODE *start = head;
    while( start->next != NULL) {
        if( start  == point) {
            start->prev->next = start->next;
            start->next->prev = start->prev;
            free( start );
            return;
        }
        start = start->next;
    }
}


void showmem()
{
    unsigned long al = 0;
    MNODE *p = head;
    while( p->next != NULL) {
        al += p->size + sizeof(MNODE);
        p = p->next;
    } 
    printf("total mem: %u\n",al);
}
