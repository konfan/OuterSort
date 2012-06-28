import socket
import sys
import time
import threading
import json
from convertd import SOCKET_FILE

def main(msg,no):
    for i in range(30):
        arg = sys.argv[1]
        data = "id:%d %s"%(no,msg)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s = sock.connect(SOCKET_FILE)
        sock.send(data)
        retstr = sock.recv(1024)
        sock.close()
        #print retstr

def sendreq(jstr):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s = sock.connect(SOCKET_FILE)
    sock.send(jstr)
    ret = ""
    retstr = sock.recv(1024 * 4)
    #print retstr
    sock.close()
    return retstr

def convertreq():
    data = {'type':'convert',
            'src':'/mnt/hgfs/RHEL6_64/videosample/gowmcollectionv10_1080.mp4',
            'dst':'/root/datatom.mkv',
            'opt':{'y':''}
            }
    jdata = json.dumps(data)
    print("Sending:%s"%jdata)
    return sendreq(jdata)

def inforeq(id = None):
    data = {'type':'info',
            'src':'/mnt/hgfs/RHEL6_64/videosample/gowmcollectionv10_1080.mp4'}
    jdata = json.dumps(data)
    print("Sending:%s"%jdata)
    return sendreq(jdata)

def progresreq(id = None):
    data = {'type':'progress',
            'id':id}
    jdata = json.dumps(data)
    print("Sending:%s"%jdata)
    return sendreq(jdata)

def heartbeatreq():
    data = {'type':'heartbeat'}
    jdata = json.dumps(data)
    recv = json.loads(sendreq(jdata)).encode('utf-8')
    if recv == 'alive':
        print('service is %s'%recv)
        return 0
    print('service failed')
    return 1

if __name__ == '__main__':
    exit(heartbeatreq())
