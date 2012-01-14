#include "sort.h" 
#include <sys/types.h>
#include <sys/stat.h>
//#include <unistd.h>


static void * mempool;
void init_map();
void readfile(char * filename);
void write_tmp_file( FILE *stream, char * target, size_t size);

int main(int argc,char * argv[])
{
    readfile( argv[1]);
}


void init_map()
{
}

FMAP * gMap;
int  tmpfilenum ;
void readfile(char * filename)
{
    /*
     * read from file,save into pieces
     */
    FILE *fp;
    char buff[BLOCK];
    struct stat sb;
    if( stat(filename, &sb) == -1) {
        perror("stat\n");
        return;
    }
    long long fsize = sb.st_size;

    tmpfilenum = fsize/S_10M + 1;
    int i;
    gMap = new( tmpfilenum * sizeof(FMAP));
    for( i=0;i<tmpfilenum;i++) {
        sprintf(gMap[i].filename,"_srt%d",i);
    }

    fp = fopen( filename,"r");
    if( !fp )
        return;

    char fname[14];
    for( i=0;i<tmpfilenum;i++) {
        sprintf(fname,"/tmp/%s",gMap[i].filename);
        write_tmp_file( fp, fname, S_10M );
    }

    fclose(fp);
}



void write_tmp_file( FILE *stream, char * target, size_t size)
{
    do {
        readc = fread( buff,1,BLOCK,fp);
        write_tmp_file( buff,readc);
    }while( !feof(fp));
    static int saved = 0;
    
}
