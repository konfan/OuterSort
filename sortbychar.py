#-*-coding:utf-8-*-

import os
S_10M = 1024*1024*10

tmpfiles = []


def readfile( fname):
    global tmpfiles
    tmpfiles = []
    size = os.path.getsize(fname)
    tmpnum = size/S_10M + 1
    for i in range(tmpnum):
        tmpfiles.append("/tmp/_sr_t"+str(i))

    fout = open(fname,'r')
    for i in range(tmpnum):
        fin = open( tmpfiles[i],'w')
        readbytes = 0
        while(True):
            line = fout.readline()
            if not line:
                fin.close()
                break
            readbytes += line.__len__()
            fin.write(line)
            if readbytes >= S_10M:
                fin.close()
                break
    fout.close()

def char_cmp(x,y):
    if x == y:
        return 0
    elif x > y:
        return -1
    else:
        return 1


def __sortfile( fname ,cmpfunc):
    print 'sort ',fname
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    for r in lines:
        r = r.lstrip().rstrip()+'\n'
    lines.sort(cmpfunc)
    f = open( fname,'w')
    for l in lines:
        f.write(l)
    f.close()



def merge( resultfile):
    def cmpfunc( l ):
        pos = 0
        m = l[0]
        for i in range(l.__len__()):
            if char_cmp(m,l[i])>0:
                pos = i
                m = l[i]
        return pos
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
    return

def sortfile( finput,foutput):
    readfile(finput)
    for s in tmpfiles:
        __sortfile( s ,char_cmp)
    merge( foutput )
    cleartmpfile()


if __name__=='__main__':
    import sys
    sortfile( sys.argv[1],sys.argv[2])


