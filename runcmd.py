#coding:utf-8
import os
import subprocess
import threading
import cStringIO


def _mkcmdline(cmdline):
    """
    make cmdline string to list
    text quoted in '"' will remain in one node
    eg: _mkcmdline('ls -ah "some dir has space'')
        -> ['ls','-ah','some dir has space']
    """
    lquote = cmdline.split('"')
    ret = []
    for i in range(len(lquote)):
        if i%2 == 0:
            ret.extend(lquote[i].split(' '))
        else:
            ret.append(lquote[i])
    return  [ x for x in ret if x != '']

def _runcmdsafe(cmdline):
    """
    safe use with subprocess.Popen
    """
    from subprocess import PIPE
    from subprocess import Popen
    cmd = _mkcmdline(cmdline)
    p = Popen(cmd,
            bufsize = 0,
            stdin = PIPE,
            stdout = PIPE,
            stderr = PIPE,
            close_fds = True)
    return p

def _runcmdunsafe(cmdline):
    """
    unsafe use with supbrocess.Popen
    may case shell injection, read python manual for more details
    """
    from subprocess import PIPE
    from subprocess import Popen
    p = Popen(cmdline,
            shell = True,
            bufsize = 0,
            stdin = PIPE,
            stdout = PIPE,
            stderr = PIPE,
            close_fds = True)
    return p

class _OWrapper(object):
    """
    an asynchronous wrapper for Popen's std I/O
    """
    def __init__(self, src):
        """
        _OWrapper(src)
        
        src is a std Output pipe, it should have a blocked read method
        """
        self._data = cStringIO.StringIO()
        self.src = src
        self._stop = False
        self._bufflock = threading.Lock()
        self._end = threading.Event()
        self._end.clear()

        self._len = 0
        self._thread = threading.Thread(target = self.handle)
        self._thread.daemon = True
        self._thread.start()

    def handle(self):
        char = '\0'
        while char != '' and (not self._stop): 
        # while char != '':
            char = self.src.read(1)
            self._bufflock.acquire()
            self._data.write(char)
            self._len += 1
            self._bufflock.release()
        self._end.set()

        #while not self._stop:
        #    char = self.src.read(1)
        #    ## char == '' means read pipe has got an EOF
        #    if char == '':
        #        self._stop = True
        #        break
        #    self._bufflock.acquire()
        #    self._data.write(char)
        #    self._len += 1
        #    l = self._len
        #    self._bufflock.release()
        ##print("end handle:%d"%l)
        #self._end.set()


    def stop(self):
        self._stop = True
        self._thread.join()

    def read(self, block = False):
        """
        read() -> string

        Return strings in buff, if nothing in buff, retun ''
        if block is True, block until read every lines from src
        otherwise return immediately(default)
        """
        if block:
            self._end.wait()
            #self._thread.join()

        strIO = self._data
        self._bufflock.acquire()
        self._data = cStringIO.StringIO()
        self._bufflock.release()
        strIO.flush()
        ret = strIO.getvalue()
        strIO.close()
        del strIO
        return ret

    def readlines(self, block = False):
        """
        readlines([block]) -> list of strings

        Return string in lines
        if block is True, block until read every lines from src
        otherwise return immediately(default)
        """
        if block:
            self._end.wait()

        strIO = self._data
        self._bufflock.acquire()
        # l = self._len
        self._data = cStringIO.StringIO()
        self._bufflock.release()
        strIO.flush()
        strIO.seek(0)
        ret = strIO.readlines()
        strIO.close()
        del strIO
        # print(''.join("has read:%d"%l))
        return ret


class CmdHandler(object):
    """
    Wrapp Popen object, provide easy controll of shell cmdline
    """
    def __init__(self, popenObj, stdout=True, stderr=True):
        """
        CmdHandler(popenObj, stdout=True, stderr = True)

        popenObj 
            a subprocess.Popen instance
        stdout
            if True, self.stdout will be wrapped by _OWrapper(default True)
        stderr
            if True, self.stderr will be wrapped by _OWrapper(default True)
        """
        # super(CmdHandler, self).__init__(arg1, argd)
        if not isinstance(popenObj, subprocess.Popen):
            raise RuntimeError("argument 1 should be a Popen instance")
        self.popen = popenObj

        self._stdin = self.popen.stdin
        if stdout:
            self._stdout = _OWrapper(self.popen.stdout)
        else:
            self._stdout = self.popen.stdout

        if stderr:
            self._stderr = _OWrapper(self.popen.stderr)
        else:
            self._stderr = self.popen.stderr

    def __del__(self):
        try:
            #self.popen.kill()
            #self._stdout.stop()
            #self._stderr.stop()
            super(CmdHandler, self).__del__()
        except:
            pass
        
    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    @property
    def stdin(self):
        return self._stdin

    def readlines(self):
        """
        readlines() -> list of strings
        a shortcut call, wait for shell cmd end
        then return stdout's output in lines
        """
        self.wait()
        return self._stdout.readlines(True)

    def read(self):
        self.wait()
        return self._stdout.read(True)

    def retvalue(self):
        """
        retvalue() -> int

        Return the shell's ret code
        if shell is running, return nothing (None)
        """
        return self.popen.poll()

    def kill(self):
        """
        kill()

        send SIG_KILL to shell cmd
        """
        self.popen.kill()

    def isfinished(self):
        """
        isfinished() -> bool

        Return True if shell cmd has end, otherwise return False
        """
        return self.popen.poll() != None

    def wait(self):
        """
        wait()

        Block until shell cmd is finished
        """
        self.popen.wait()


def popen(cmdline):
    """
    popen(cmdline, [setstderr]) -> CmdHandlerObj

    Return a CmdHandler object, run shell command 'cmdline' in safe mode
    """
    return CmdHandler(_runcmdsafe(cmdline))

def popenunsafe(cmdline):
    """
    popenunsafe(cmdline, [setstderr]) -> CmdHandlerObj

    Return a CmdHandler object, run shell command 'cmdline' in unsafe mode
    """
    return CmdHandler(_runcmdunsafe(cmdline))


def setup():
    try:
        import setuptools
    except ImportError:
        print("require python-setuptools")
        return 1

    # dstfile = os.path.split(setuptools.__file__)[0] + '.pth'
    dstfile = os.path.dirname(setuptools.__file__)
    dstfile = os.path.abspath(os.path.join(dstfile, '..', 'runcmd.py'))
    # moduledir = os.path.abspath(os.path.dirname(__file__))
    srcfile = os.path.abspath(__file__)
    if not os.path.isfile(srcfile):
        print("could not open %s"%srcfile)
        return 1

    popenunsafe("/bin/cp %s %s && /bin/rm %sc"%(srcfile, dstfile, dstfile))
    # popenunsafe("cat %(pth)s |grep -v %(curdir)s > %(pth)s.bak && \
    #             echo %(curdir)s >> %(pth)s.bak && \
    #             /bin/mv %(pth)s.bak %(pth)"
    #             %{"pth":dstfile, "curdir":moduledir})
    os.chdir('/tmp')
    try:
        import runcmd
    except:
        print("install failed")
        return 1
    else:
        print("install succeed")
        return 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("use 'python runcmd.py install' to install this module")
        exit(1)
    elif sys.argv[1] != 'install':
        print("use 'python runcmd.py install' to install this module")
        exit(1)
    else:
        setup()
