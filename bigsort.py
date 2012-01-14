#-*-coding:utf-8-*-
import gb2utf8
import sortbychar
import countkeys
import os


def main( input,output):
    import time
    starttime = time.time()
    sortbychar.sortfile( input,'/tmp/_sr_sortkeys')
    countkeys.countkeys('/tmp/_sr_sortkeys',output)
    os.remove('/tmp/_sr_sortkeys')
    print 'run time ',str( time.time() - starttime)

if __name__ == '__main__':
    import sys
    main(sys.argv[1],sys.argv[2])
