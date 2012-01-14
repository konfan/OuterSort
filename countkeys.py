#-*-coding:utf-8-*-

import os
S_10M = 1024*1024*10

tmpfiles = []


def readfile( fname):
    global tmpfiles
    tmpfiles = []
    fout = open(fname,'r')
    fseq = 0
    finished = False
    cache = ""
    counts = 0
    while not finished:
        tmpfiles.append("/tmp/_sr_t"+str(fseq))
        fin = open( tmpfiles[fseq],'w')
        writebytes = 0
        while True:
            line = fout.readline()
            if not line:
                finished = True
                fin.write( "%10d:%s"%(counts,cache))
                break
            if( line == cache):
                counts += 1
                continue
            else:
                if cache:
                    fin.write( "%10d:%s"%(counts,cache))
                    writebytes += cache.__len__() + 11
                counts = 1
                cache = line
                if writebytes >= S_10M:
                    break
        fin.close()
        fseq += 1
    fout.close()


def int_cmp(x,y):
    if x[0] == y[0]:
        return 0
    elif x[0] >  y[0]:
        return -1
    else:
        return 1


def decodeline( line ):
    pos = line.find(':')
    if pos >= 0:
        return int(line[:pos]),line[pos+1:]
    return 0,""



def sortfile( fname,cmpfunc ):
    print 'sort ',fname
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    tmpl = [ decodeline(x) for x in lines]
    tmpl.sort( cmpfunc) 
    f = open( fname,'w')
    for l in tmpl:
        f.write("%10d:%s"%(l[0],l[1]))
    f.close()


def getMostUse( l ):
    pos = 0
    mNum = 0
    for index in range(l.__len__()):
        num,line = decodeline( l[index] )
        #if mNum < num
        #if int_cmp( (0,mNum),(0,num))>0:
        if mNum < num:
            mNum = num
            pos = index
    return pos

def merge( resultfile, cmpfunc):
    print 'merge'
    global tmpfiles
    print tmpfiles
    fplist = [ open(x,'r') for x in tmpfiles]
    fsorted = open(resultfile,'w')
    firstlines = [ x.readline() for x in fplist ]
    count = 0
    while [ u for u in firstlines if u]:
        pos = cmpfunc( firstlines )
        fsorted.write( firstlines[pos])
        firstlines[pos] = fplist[pos].readline()
        count += 1
        if count % 100000 == 0:
            print 'write %d lines'%count
        
    fsorted.close()
    for f in fplist:
        f.close()
    return

def cleartmpfile():
    for x in tmpfiles:
        os.remove(x)

def countkeys( fsortedfile, foutfile):
    readfile( fsortedfile)
    for s in tmpfiles:
        sortfile( s ,int_cmp)
    merge(foutfile, getMostUse)
    cleartmpfile()


if __name__ == '__main__':
    import sys
    countkeys(sys.argv[1],sys.argv[2])

