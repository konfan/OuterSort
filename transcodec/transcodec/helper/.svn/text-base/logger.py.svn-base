#coding:utf-8
import logging
import logging.handlers

DBLOGFILE = '/tmp/convert.debug'
LOGFILE = '/tmp/convert.log'

def initlog():
    dbglogger = logging.getLogger('convertd')
    dbglogger.setLevel(logging.DEBUG)

    dh = logging.handlers.RotatingFileHandler(
                DBLOGFILE, maxBytes = 1024*1024*5, backupCount = 5)

    formatter = logging.Formatter(
                    fmt = '%(asctime)s:\t%(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S')
    dh.setFormatter(formatter)
    dbglogger.addHandler(dh)

    logger = logging.getLogger('convertlog')
    logger.setLevel(logging.INFO)
    ih = logging.handlers.RotatingFileHandler(
                LOGFILE, maxBytes = 1024*1024*5, backupCount = 5)
    ih.setFormatter(formatter)
    logger.addHandler(ih)


def debug(message):
    logger = logging.getLogger('convertd')
    if not logger.handlers:
        initlog()
    logger.debug(message)

def info(message):
    logger = logging.getLogger('convertlog')
    if not logger.handlers:
        initlog()
    logger.info(message)
