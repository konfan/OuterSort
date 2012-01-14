#-*-coding:utf-8-*-

import os

def mdcode( s ):
    try:
        for c in ['gbk','gb2312']:
            return s.decode(c).encode('utf-8')
    except:
        pass
    return s

def convert(filein,fileout):
    fin = open(filein,'r')
    fo = open(fileout,'w')
    line = fin.readline()
    while line:
        fo.write( mdcode(line))
        line = fin.readline()
    fin.close()
    fo.close()

if __name__=='__main__':
    import sys
    convert(sys.argv[1],sys.argv[2])
