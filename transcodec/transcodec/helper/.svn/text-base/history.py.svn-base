# coding:utf-8
import cPickle
import os
import sys
import logger


def savetofile(obj, fname):
    if not obj:
        return
    #logger.debug(dir(obj))
    #logger.debug(type(obj))
    #logger.debug(obj.__class__)
    try:
        f = open(fname, 'a+')
        cPickle.dump(obj, f, 2)
        f.close()
    except IOError:
        f.close()


def loadfromfile(fname):
    try:
        ret = []
        f = open(fname, 'r')
        while True:
            ret.append(cPickle.load(f))
    except EOFError:
        f.close()
        return ret
    except IOError:
        return ret

# TODO: here is a simple version 
#       write all data to one file and load all data to memory at one time
#       should be improved later

old_history_key = []

def getfiletosave():
    return '/tmp/convert_history'

def getfiletoread(opt):
    return '/tmp/convert_history'

def save(hlist):
    global old_history_key
    f = getfiletosave()
    # get diff 
    diff = dict([(x,hlist.get(x)) for x in hlist.keys() if x not in old_history_key])
    savetofile(diff, f)
    old_history_key = hlist.keys()

def load(readopt):
    f = getfiletoread(readopt)
    hlist = loadfromfile(f)
    ret = {}
    map(ret.update, hlist)
    old_history_key = ret.keys()
    return ret

