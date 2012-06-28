#coding: utf-8
import sys
sys.path.append('..')
from engine import media_engine
import time
import sys
import os




def benchmark(file):
	def getdst(f):
		r,n = os.path.split(f)
		return os.path.join(r, 
				"_trans%s.mkv"%os.path.splitext(n)[0])
	starttime = time.time()
	print("start time %s"%time.ctime())
	print("convert %s"%file)
	handle = media_engine.convertmedia(
				file,
				getdst(file),
				{"y":"","vcodec":"libvpx",
                    "b:v":"500k","strict":"-2",
                    "f":"webm","cpu-used":"5"})
	handle.wait()
	endtime = time.time()
	print("used time %d\n"%(endtime - starttime))

defaultp = "/dcache/videotest"

def main(dir):
	import os
	if os.path.isfile(dir):
		benchmark(dir)
	else:
		map(main, map(lambda x: os.path.join(dir,x), os.listdir(dir))) 

if __name__ == '__main__':
	if len(sys.argv) == 1:
		#main(defaultp)
		print("usage: python testConvert.py dir")
	elif os.path.isdir(sys.argv[1]):
		main(sys.argv[1])
	else:
		print("usage: python testConvert.py dir")
