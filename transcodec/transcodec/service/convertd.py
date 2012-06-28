#!/usr/bin
# coding=utf-8

import os, sys, SocketServer, threading
import uuid
from daemon import runner

__moduledir__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.abspath(__moduledir__))

import convertservice
from helper import *
from helper.sematool import *
from helper import jsontool
from helper import history
from helper import logger
from engine import media_engine
from engine import doc_engine


###### unix_socket file ######
SOCKET_FILE = '/tmp/convertd_socket'
###### request ######
MAX_REQ_LENGTH = 20
REQ_FULL = "REQ_FULL"
REQ_INVALID = "REQ_INVALID"
REQ_INVALID_ID = "REQ_INVALID_ID"
REQ_EXIST_CONVERT = "REQ_EXIST_CONVERT"

###### task ######
MAX_TASK_LENGTH = 10
TASK_NOT_START = "TASK_NOT_START"
TASK_PROGRESS = "TASK_PROGRESS: %s"
TASK_FINISHED = "TASK_FINISHED"
TASK_FAILED = "TASK_FAILED: RETURN %d"
TASK_CANCEL_FAILED = "TASK_CANCEL_FAILED %s"
TASK_CANCELED = "TASK_CANCELED %s"

###### heartbeat ######
HEARTBEAT = "alive"

###### req constraint ###### not done yet
req_token = "CONVERTD_CONSTRAINT_TOKEN"
req_kvmap = {
        "type":["convert","list","info","progress","cancel","heartbeat"],
        "engine":["media","document"],
        "id":[req_token],
        "src": [req_token],
        }
req_vkmap = {
        "convert": ["engine", "src"],
        "info": ["engine|id","src"],
        "progress": ["id"],
        "cancel": ["id"],
        "media": ["src"],
        "document": ["src"],
        }


task_list = {}
request_list = {}
history_list = history.load('')

_semaphore_task = semaphore_init(MAX_TASK_LENGTH, MAX_TASK_LENGTH)
_semaphore_req = semaphore_init(MAX_REQ_LENGTH, 0)

_cfgfile = os.path.abspath(os.path.join(__moduledir__, 'config.conf'))
opttool.load(_cfgfile, optconfig.env)
_default_opt = optconfig.config

def _free_task_list():
    logger.debug('task_list.key : %s'%task_list.keys())
    for k in task_list.keys():
        handle = task_list.get(k).handle
        assert(hasattr(handle,'isfinished'))
        if hasattr(handle,'isfinished'):
            # handle is returned by engine and should have a isfinished method
            if handle.isfinished():
                logger.info('%s finished, return %d'%(
                            task_list[k].get('src'),
                            handle.retvalue()))
                tmp = dict(task_list.pop(k))
                history_list[k] = tmp
                sema_signal(_semaphore_task)
                tmp['ret'] = handle.retvalue()
                # TODO: here only save dict to file
                #       prefer history like this: 
                #           write_to_history( id, engine, src, status, time)
                history.save(history_list)
    

def checkone(obj, key):
    def checkvkmap(lst):
        if lst == None:
            return [True]
        return map(lambda z:checkone(obj,z), lst)

    if len(key.split('|')) > 1:
        return reduce(lambda x,y:x or y, 
                        checkvkmap(key.split('|')))
    #checkkvmap
    v = obj.get(key)
    if v == None:
        return False

    if req_kvmap.get(key) == [req_token]:
        return type(v) == type('string')

    elif v  not in req_kvmap.get(key):
        return False
    
    return reduce(lambda x,y:x and y,
                    checkvkmap(req_vkmap.get(v)))


def checkreq(obj):
    """
    check obj is valid request
    """
    if not obj.has_key('type'):
        return False

    if obj.get('src'):
        if not os.path.isfile(obj.get('src')):
            return False

    return checkone(obj, 'type')


class _SocketHandler(SocketServer.BaseRequestHandler):
    """
    socket request handler
    dispatch request to correct list
    send response message back
    call by SocketServer's main thread
    """
    # TODO: handle request by different engine

    def handle(self):
        # check the finished task on request in
        _free_task_list()

        data = self.request.recv(1024*4).strip()
        logger.debug( "recv a req, save it %s"%data)
        logger.info("recived: %s"%data)


        try:
            st_data = jsontool.decode(data)
        except:
            logger.debug("req is invalid json:%s"%data)
            logger.info("req is invalid json:%s"%data)
            self.request.send(jsontool.encode(REQ_INVALID))
            return

        # req format is not correct
        if not checkreq(st_data):
            logger.debug("check req failed: %s"%str(st_data))
            logger.info("check req failed: %s"%str(st_data))
            self.request.send(jsontool.encode(REQ_INVALID))
            return

        try:
            # logger.debug('in handle st_data is %s, type:%s'%(str(st_data), type(st_data)))
            f = self._get_f(st_data.get('type'))
            f(self, st_data)


            logger.debug("request list: %s"%str(request_list))
            logger.debug("task list: %s"%str(task_list))
            logger.debug("history list: %s"%str(history_list))
        except Exception, e:
            logger.info("Error: %s"%str(e))
            logger.debug("Error: %s"%str(e))

    etable = {
            'media': media_engine,
            'document':doc_engine,
            }
    def getengine(self, data):
        if data.has_key('engine'):
            return self.etable.get(data.get('engine'))
        else:
            key = data.get('id')
            return self.etable.get(task_list.get(key).get('engine'))

    def convert_req(self, data):
        # request_list is full
        if len(request_list) >= MAX_REQ_LENGTH:
            self.request.send(jsontool.encode(REQ_FULL))
            return

        for i,d in request_list.items():
            if d.get('src',"$") == data.get('src'):
                self.request.send(jsontool.encode(i))
                return

        if data.get('src') in [x.get('src') for x in task_list.values()]:
            self.request.send(jsontool.encode(REQ_EXIST_CONVERT))
            return

        id = uuid.uuid4().hex
        request_list[id] = data
        sema_signal(_semaphore_req)
        self.request.send(jsontool.encode(id)) # send result back
    
    def info_req(self, data):
        ## TODO: a cache is better
        #if hasattr(data, 'id'):
        #    listname, task = search3list(data.id)
        #    if wrong:
        #        sendback error
        #    if task has info:
        #        sendback task.info
        #info = media_engine.getmediainfo(data['src'])
        info = self.getengine(data).getinfo(data['src'])
        self.request.send(jsontool.encode(info))

    def progress_req(self, data):
        logger.debug('progress req:%s'%str(data))
        logger.info("progress req:%s"%data)
        if not data.has_key('id'):
            self.request.send(jsontool.encode(REQ_INVALID_ID))
            return
        id = data.get('id')

        if request_list.has_key(id):
            self.request.send(jsontool.encode(TASK_NOT_START))
            return

        elif task_list.has_key(id):
            task = task_list.get(id)
            try:
                #p = media_engine.getprogress(task.handle)
                p = self.getengine(data).getprogress(task.handle)
            except AttributeError:
                self.request.send(jsontool.encode(TASK_NOT_START))
            self.request.send(jsontool.encode(TASK_PROGRESS%p))
            return

        elif history_list.has_key(id):
            # in history_list, data has been convert to origin dict
            data = history_list.get(id)
            assert(data.has_key('ret'))
            if data['ret'] == 0:
                self.request.send(jsontool.encode(TASK_FINISHED))
            else:
                self.request.send(jsontool.encode(TASK_FAILED % data['ret']))
            return

        else:
            self.request.send(jsontool.encode(REQ_INVALID_ID))



    def tasklist_req(self, data):
        # send {'id','src'} dict back
        # f = lambda dic: map(lambda key:(key,dic[key].get('src','N/A')), dic.keys())
        def f(dic):
            ret = {}
            for k in dic.keys():
                ret[k] = dic[k]
            return ret
        logger.debug('in tasklist_req: data is %s'%str(data))
        ret = {'wait_list':{}, 'convert_list':[], 'history_list':[]}
        ret['wait_list'].update(f(request_list))

        #t = lambda handle: "%ds"%(self.getengine(data).getprogress(handle))
        #map(ret['convert_list'].append, 
        #    [[key, task_list[key].get('src'), t(task_list[key].handle)] for key in task_list.keys()]
        #    )
        def t(key):
            d = task_list.get(key)
            return self.getengine(d).getprogress(d.handle)

        for key in task_list.keys():
            src = task_list[key].get('src')
            ret['convert_list'].append([key, src, t(key)])

        for key in history_list.keys():
            src = history_list[key].get('src')
            rval = history_list[key].get('ret', 1)
            ret['history_list'].append([key, src, rval])

        self.request.send(jsontool.encode(ret))


    def cancel_req(self, data):
        # handle() is a block call
        # so there's no multi-thread problem here
        id = data.get('id','validid')
        
        if request_list.has_key(id):
            request_list.pop(id)
            ret = TASK_CANCELED % id

        elif task_list.has_key(id):
            task = task_list.get(id)
            try:
                task_list.pop(id)
            except KeyError:
                ret = TASK_CANCEL_FAILED % id
            else:
                if task != None:
                    task.handle.kill()
                    ret = TASK_CANCELED % id
        else :
            ret = REQ_INVALID
        self.request.send(jsontool.encode(ret))

        
    def heartbeat_req(self, data):
        self.request.send(jsontool.encode(HEARTBEAT))

    _req_dispatch_table = {
            'convert': convert_req,
            'info': info_req,
            'progress': progress_req,
            'list': tasklist_req,
            'cancel': cancel_req,
            'heartbeat':heartbeat_req,
            }


    def _get_f(self, reqtype):
        return self._req_dispatch_table.get(reqtype)


class DictWrapper(dict):
    """
    make dict obj modifiable
    """
    pass



class TaskHandler(object):
    """
    handle task request of convert
    """
    def __init__(self):
        self._thread = threading.Thread(target = self._handle_request)
        self._thread.daemon = True
        
    def start(self):
        self._thread.start()

    def stop(self):
        """
        kill the convert process
        """
        for data in task_list.values():
            #logger.debug('kill %s'%str(data))
            if hasattr(data, 'handle'):
                try:
                    data.handle.kill()
                    data.handle.retvalue()
                    logger.debug("kill pid %d src file %s"%(data.handle.pid, data.get('src','N/A')))
                    logger.info("kill pid %d src file %s"%(data.handle.pid, data.get('src','N/A')))
                except Exception, e:
                    logger.debug("except while kill %s %s"%(data['src'], str(e)))

    def _convert_media(self, data):
        opts = _default_opt[data.get('engine','media')].copy()
        opts.update(data.get('opt',{}))

        # dst file is in the same dir of src file
        # with a prefix name _low and ext name change to .webm
        folder, filename = os.path.split(data['src'])
        basename, extname = os.path.splitext(filename)
        data['dst'] = os.path.join(folder, "%s_low.%s"%(basename,'webm'))
        logger.info(media_engine._makeffmpegcmd(data['src'], data['dst'], opts))

        # call engine 
        h = media_engine.convertmedia(data['src'], data['dst'], opts)
        return h


    def _convert_doc(self, data):
        opts = None
        folder, filename = os.path.split(data['src'])
        basename, extname = os.path.splitext(filename)
        data['dst'] = os.path.join(folder, "%s.%s"%(basename,'pdf'))
        logger.info(doc_engine._makeunoconvcmd(data['src'], data['dst'], opts))

        # call engine 
        h = doc_engine.convertdoc(data['src'], data['dst'], opts)
        return h

    engine_function = {'media': _convert_media,
                        'document': _convert_doc,
                        }

    def _handle_request(self):
        """
        get req from request_list
        run convert synchronous and put handles in task_list
        """
        while True:
            # wait for task finished
            sema_wait(_semaphore_task) 
            # wait request
            sema_wait(_semaphore_req) 
            id, d = request_list.popitem()
            data = DictWrapper(d)
            try:
                logger.debug('recv data: %s'%str(data))
                data.handle = self.engine_function[data.get('engine')](self,data)
            except Exception,e:
                logger.info(e)
            task_list[id] = data


class ServiceImp(object):
    """
    implement run and stop method for convertservice
    """
    def __init__(self, 
                 stdout = '/dev/null', 
                 stderr = '/dev/null',
                 pidfile = '/tmp/convertd.pid'):
        self.stdin_path = '/dev/null'
        self.stdout_path = stdout
        self.stderr_path = stderr
        self.pidfile_path = pidfile
        self.pidfile_timeout = 0
        self.socketserver = None
        self.taskhandler = TaskHandler()

    def run(self):
        self.taskhandler.start()
        self.raiseserver()

    def stop(self):
        self.taskhandler.stop()

    def raiseserver(self):
        try:
            os.remove(SOCKET_FILE)
        except OSError:
            pass
        self.socketserver = SocketServer.UnixStreamServer(SOCKET_FILE, _SocketHandler)
        self.socketserver.serve_forever()


out_f = '/dev/null'

def main():
    app = ServiceImp(stdout = out_f, 
                     stderr = out_f)
    drunner = convertservice.ConvertService(app)
    try:
        drunner.do_action()
    except Exception, e:
        logger.info("%s"%str(e))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("usage: python convertd.py start|restart|stop\n")
    elif sys.argv[-1] == 'debug':
        out_f = '/dev/tty'
        sys.argv.pop(-1)
        main()
    else:
        main()
