# encoding:UTF-8
# media_engine v0.9
import os
import subprocess
import re
import sys
import runcmd
from helper import logger


def gbtoutf8(sgb):
    """
    transcode gb str to utf8
    """
    try:
        for c in ['gbk','gb2312']:
            return sgb.decode(c).encode('utf-8')
    except:
        pass
    return sgb


def _getmediainfo(stdpipe):
    """
    return the media info from input
    """
    def __infostrtodict(strlst):
        r = {}
        ptype = re.compile(r'Input #\d+, (.+), from') 
        pduration = re.compile(r'Duration:\s*(\d+[0-9]:[0-5][0-9]:[0-5][0-9])')
        pbitrate = re.compile(r'Duration:.+bitrate:\s*(\d+ kb/s)')
        presolution = re.compile(r'Video.+, (\d+x\d+), ')
        pvideo = re.compile(r'Video: (.+?), ')
        paudio = re.compile(r'Audio: (.+?), ')
        keymap = {'type':ptype,
                  'duration':pduration,
                  'bitrate':pbitrate,
                  'resolution':presolution,
                  'video':pvideo,
                  'audio':paudio,
                  }
        for k,v in keymap.items():
            for x in strlst:
                try:
                    r[k] = v.search(x).groups()[0]
                except:
                    if not r.has_key(k):
                        r[k] = 'Unknown'

        r['detail'] = strlst
        return r

    assert file == type(stdpipe)
    lines = map(gbtoutf8, stdpipe.readlines())
    lst = []
    for x in range(len(lines)):
        pos = lines[x].find("Input")
        if pos >= 0:
            lst = lines[x:]
            break
    return __infostrtodict(lst)


def getinfo(fname):
    """
    get media files info
    """
    fpath = os.path.abspath(fname);
    if not os.path.isfile(fpath):
        raise Exception("%s is not a valid file"%(fpath))

    fprobe = "ffprobe %s"%(fpath.replace(' ',r'\ '))
    #pro, s_in, s_err = _runcmd(fprobe)
    handle = runcmd.CmdHandler(runcmd._runcmdunsafe(fprobe),
                                stdout = False,
                                stderr = False)
    handle.wait()
    return _getmediainfo(handle.stderr)


def _makeffmpegcmd(inputfile, outputfile, opts):
    """
    generate command line for ffmpeg, using options in opts
    return cmd string
    """
    #ffmpeg -i inputfile -opts -opts -opts outputfile
    f = lambda x: " ".join(["-%s %s"%(k,str(v)) for k,v in x.items()])
    ret = "ffmpeg -i %(input)s %(opt)s %(output)s"%{
                "input":inputfile.replace(' ',r'\ '),
                "output":outputfile.replace(' ',r'\ '),
                "opt":f(opts)
            }
    return ret


def convertmedia(src, dst, opts):
    """
    read src file, convert format to dst file
    format detail is set in opts
    """

    cline = _makeffmpegcmd(src, dst, opts)
    print(cline)
    handle = runcmd.CmdHandler(runcmd._runcmdunsafe(cline), stdout = False, stderr = True)
    return handle

def cancelconvert(handle):
    """
    cancel the convert process by handle
    """
    handle.kill()
    return handle.wait()

def getprogress(handle):
    """
    query handle's convert progress
    """
    if not hasattr(handle, "curtime"):
        handle.curtime = 0
    
    # try to read output
    delimiter = '\r\n'
    output = handle.stderr.read()
    if output == '':
        return handle.curtime

    # reverse the output, try to get the last line's progress
    lines = re.split(r'[\r\n]', output)[::-1]
    pattern = re.compile(r'\d+[0-9]:[0-5][0-9]:[0-5][0-9]')
    str_cur_time = ""
    cur_time = 0
    for l in lines:
        if l.find("time=") >= 0:
            m = pattern.search(l)
            if not m:
                continue
            str_cur_time = m.group()
            scale = 3600
            cur_time = 0
            for t in str_cur_time.split(":"):
                cur_time += scale * int(t)
                scale = scale / 60
            if cur_time > handle.curtime:
                handle.curtime = cur_time
                break
            else:
                continue
    return "%d s"%handle.curtime


def main():
    fname = "/mnt/hgfs/RHEL6_64/videosample/gowdv.dv"
    tmpopt = {"vcodec":"libvpx", "y":""}
    infile = "gowmcollectionv10_1080.mp4"
    outfile = "pyotest.avi"
    s = getmediainfo(fname)
    for x in s:
        print x[:-1]

testsrc = '/root/Videos/gowshort.mp4'
testdst = '/root/Videos/gowshort_low.webm'
testopt = {'vcodec':'libvpx', 'strict':'-2', 'f':'webm','y':' ', 'b:v':'500k','cpu-used':'5'}

def test():
    import time
    h = convertmedia(testsrc, testdst, testopt)
    return h

if __name__ == "__main__":
    main()
