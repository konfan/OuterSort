# coding:utf-8

from service import convertreq
from helper import jsontool
import os

def wrappreq(req):
    recv = convertreq.sendreq(jsontool.encode(req))
    ret = jsontool.decode(recv)
    if hasattr(ret, 'encode'):
        ret = ret.encode('utf-8')
    return ret


def testlist():
    req = {'type':'list'}
    ret = wrappreq(req)
    assert(ret.has_key('wait_list'))
    assert(ret.has_key('convert_list'))
    assert(type(ret['wait_list']) == type({}))
    assert(type(ret['convert_list']) == type([]))
    return ret

def testinfo(src):
    req = {'type':'info', 'engine':'media', 'src':src}
    ret = wrappreq(req)
    return ret


def testprogress(id):
    req = {'type':'progress','id':id}
    return wrappreq(req)


def testconvert(src):
    req = {'type':'convert','src':src, 'engine':'media'}
    return wrappreq(req)



def testcancel(id):
    req = {'type':'cancel','id':id}
    return wrappreq(req)


def main():
    print(testlist())


if __name__ == '__main__':
    main()
