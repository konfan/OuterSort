#include <stdio.h>
#include <pthread.h>
#include <string.h>


pthread_mutex_t list_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t list_cond = PTHREAD_COND_INITIALIZER;

int gi = 0;
void * main_thread(void *);
int main()
{
    pthread_t thinfo;
    memset( &thinfo,0,sizeof(thinfo));
    pthread_create( &thinfo,NULL,main_thread,NULL);
    sleep(4);
    while(1){
        pthread_mutex_lock( &list_mutex );
        pthread_cond_wait( &list_cond, &list_mutex );
        printf("main awaked %d\n",gi);
        pthread_mutex_unlock( &list_mutex );
    }
    return 0;
}


void * main_thread(void *arg)
{		
    while(1) {
        //generate cache data to java obj
        printf("thread awaked %d\n",gi++);
        pthread_mutex_lock( &list_mutex );
        pthread_cond_signal( &list_cond );
        pthread_mutex_unlock( &list_mutex );
        sleep(3);
    }    
    return NULL;
}


