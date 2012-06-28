# coding:utf-8
# doc_engine v0.1 2012.6.19
import os
import subprocess
import re
import sys
import runcmd
from helper import logger

def _makeunoconvcmd(src, dst = None, opts = None):
    """
    _makeunoconvcmd(src, dst, opts) -> string

    Return a unoconv command string
    src is input file's absolute path, dst and opts are not used
    """
    return "python /usr/bin/unoconv -fpdf %s"%src

def convertdoc(src, dst, opts):
    """
    convertdoc(src, dst, opts) -> runcmd.CmdHandler

    Return a shell handle
    src is input file's absolute path. dst and opts are not used
    """
    cline = _makeunoconvcmd(src, dst, opts)
    handle = runcmd.CmdHandler(runcmd._runcmdsafe(cline), False, False)
    return handle

def cancelconvert(handle):
    """
    cancelconvert(handle) -> None

    Cancel handle's task
    """
    handle.kill()
    return handle.wait()


def getprogress(handle):
    """
    getprogress(handle) -> string

    Return handle's progress in string
    now only return "converting" and "finished"
    """
    if not handle.isfinished():
        return "converting"
    return "finished"

def getinfo(fname):
    """
    getinfo(fname) -> string

    Return fname's detail info
    not implement now
    """
    return "have not implemented, wait for further update"
