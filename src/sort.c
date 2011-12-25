#include "sort.h" 
//#include <unistd.h>


static void * mempool;
void init_map();

int main(int argc,char * argv[])
{

    while( 1 ) {
        FMAP *p = new(sizeof( 1024 * 1024 * 10));
        delete(p);
    }
    return 0;
}


void init_map()
{
}
