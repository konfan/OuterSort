#-*-coding:utf-8-*-

import os
S_10M = 1024*1024*10

tmpfiles = []

def mdcode( s ):
    try:
        for c in ['gbk','gb2312']:
            return s.decode(c).encode('utf-8')
    except:
        pass
    return s

def readfile( fname):
    size = os.path.getsize(fname)
    tmpnum = size/S_10M + 1
    tmpfiles = []
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
    if x[0] == y[0]:
        return 0
    elif x[0] > y[0]:
        return -1
    else:
        return 1

def int_cmp(x,y):
    if x[1] == y[1]:
        return 0
    elif x[1] >  y[1]:
        return -1
    else:
        return 1


def sortfile( fname ,cmpfunc):
    f = open(fname,'r')
    lines = f.readlines()
    f.close()
    dic = {}
    for r in lines:
        s = mdcode(r.lstrip().rstrip())
        s = s + '\n'
        if dic.has_key(s):
            dic[s] += 1
        else:
            dic[s] = 1
    lines = dic.items()
    lines.sort( cmpfunc) 
    f = open( fname,'w')
    for l in lines:
        f.write("%10d : %s"%(l[1],l[0]))
    f.close()

def decodeline( line ):
    pos = line.find(':')
    if pos >= 0:
        return int(line[:pos]),line[pos+2:]
    return 0,""


def getTopLine( l ):
    pos = 0
    mLine = ""
    for index in range(l.__len__()):
        num,line = decodeline( l[index] )
        if char_cmp( (mLine,0),(line,0))>0:
            mLine = line
            pos = index
    return pos 

def getMostUse( l ):
    pos = 0
    mLine = ""
    mNum = 0
    for index in range(l.__len__()):
        num,line = decodeline( l[index] )
        if int_cmp( (mLine,mNum),(line,num))>0:
            mLine = line
            mNum = num
            pos = index
    return pos

def merge( resultfile, cmpfunc):
    print 'merge'
    fplist = [ open(x,'r') for x in tmpfiles]
    fsorted = open(resultfile,'w')
    firstlines = [ x.readline() for x in fplist ]

    count = 0
    writebuff = ""
    while [ u for u in firstlines if u]:
        pos = cmpfunc( firstlines )
        num,l = decodeline(writebuff)
        x,y = decodeline( firstlines[pos])
        firstlines[pos] = fplist[pos].readline()
        #if y.find("123456789")>0:
        #    print y,l
        if y == l:
            writebuff = "%10d : %s"%( num+x, y)
            continue
        else:
            writebuff = "%10d : %s"%( x,y)
        fsorted.write( writebuff)
        count += 1
        if count % 100000 == 0:
            print 'write %d lines'%count
        
    fsorted.close()
    for f in fplist:
        f.close()
    return


if __name__ == '__main__':
    import sys
    readfile(sys.argv[1])
    for s in tmpfiles:
        sortfile( s ,char_cmp)
#    tmpfiles = [ "/tmp/_sr_t"+str(x) for x in range(2)]
    merge('/tmp/_sr_uniqkeys', getTopLine)
    readfile( '/tmp/_sr_uniqkeys')
    for s in tmpfiles:
        sortfile( s, int_cmp)
    merge('results', getMostUse)



