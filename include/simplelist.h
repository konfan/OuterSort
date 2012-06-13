#ifndef _SIMPLE_DLIST_H
#define _SIMPLE_DLIST_H

/**
 * Simple doubly linked list 
 * 
 * entry is node type
 */
struct entry {
    struct entry *prev;
    struct entry *next;
};

/**
 * list head
 * @prev: the first node in list 
 * @next: the last node in list
 * first == end == head: list is empty
 */
typedef struct entry entry_head;

/**
 * Create a list head
 * 
 * return a head node, prev and next point to head itself
 * or return NULL if failed
 */
static entry_head * list_init( )
{
    entry_head * h = ( entry_head *)calloc(1,sizeof( entry_head ));
    if( h != NULL ) {
        h->prev = h;
        h->next = h;
        return h;
    }
    return NULL;
}

/**
 * Insert a new entry on tail
 *
 * @head: list's head
 * @new: entry to insert in
 */
static void list_add( entry_head *head, struct entry *new ) 
{
    struct entry * end = head->next;
    new->prev = end;
    new->next = head;
    end->next = new;
    head->next = new;
    if( head->prev == head)
        head->prev = new;
}

/**
 * Cut and return the first node
 *
 * @head: list's head
 * return the first node,if list is empty return head
 */
static struct entry * list_cut_first( entry_head *head ) 
{
    struct entry * first = head->prev;
    head->prev = first->next;
    if( head->prev == head )
        head->next = head;
    return first;
}

#endif
