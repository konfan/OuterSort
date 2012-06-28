#-*-coding:utf-8 -*-

import sys
import os.path

class Config(dict):
    def __getattr__(self, name):
        return self[name]

config = Config({
    "media":Config({
        })
    })

def Media(**args):
    config["media"]["cpu-used"] = "5"
    config["media"]["b:v"] = "500k"
    config["media"].update(args)
    #config["media"].get("fps",30)


env = {"media":Media}
FULLPATH = lambda fname: os.path.join(
                    os.path.abspath('.'),
                    fname)
