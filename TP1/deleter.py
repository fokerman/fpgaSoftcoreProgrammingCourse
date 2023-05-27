#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, stat, sys, re, shutil

IGNORE_LIST = ['.svn', 'bin', 'deleter.py']
IGNORE_EXT = ['.o', '.bin', '.elf', '.txt', '.bmp', '.out']
CLEAN_EXT = ['.c', '.asm', '.h', 'Makefile']

def walktree(top="", depthfirst=False):
	try:
		tst = os.lstat(top if top else '.')
	except os.error:
		tst = None
	if not depthfirst:
		yield tst,top

	if stat.S_ISDIR(tst.st_mode):
		names = os.listdir(top if top else '.')
		for name in names:
			try:
				st = os.lstat(os.path.join(top, name) if top else name)
			except os.error:
				continue
			newtop = os.path.join(top, name) if top else name
			if any(name.endswith(ext) for ext in IGNORE_EXT):
				continue
			if name not in IGNORE_LIST:
				for x in walktree (newtop, depthfirst):
					yield x
	if depthfirst:
		yield tst,top

#~ DEL_START = r'.*/[/\*] *<<<REMOVE>>>.*'
DEL_START = r'.*[;\//\/*\#] *<<<REMOVE BEGIN>>>'
#~ DEL_END   = r'.*/[/\*] *<<<REMOVE END>>>.*'
DEL_END   = r'.*[;\//\/*\#] *<<<REMOVE END>>>'

def deleterto(src, dst):
	if not os.path.exists(dst):
		os.makedirs(dst, mode=0o755)
	for st,fn in walktree(src):
		nfn = os.path.join(dst, fn)
		print(fn)
		if stat.S_ISDIR(st.st_mode):
			if not os.path.exists(nfn):
				os.mkdir(nfn, 0o755)
		else:
			in_delete = False
			nf = open(nfn, 'w')
			nl = 0
			for l in open(fn, 'r'):
				nl += 1
				if re.match(DEL_START, l, re.IGNORECASE):
					if in_delete:
						print("WARNING: %s:%d nested delete sections not supported.")
					in_delete = True
				if not in_delete or not any(fn.endswith(ext) for ext in CLEAN_EXT):
					#~ print (l)
					nf.write(l)
				if re.match(DEL_END, l, re.IGNORECASE):
					if not in_delete:
						print ("WARNING: %s:%d nested delete sections not supported.")
					in_delete = False
			nf.close()
			shutil.copystat(fn,nfn)
			
			

def main(argv):
	if len(argv) != 3:
		print ("USO: " + argv[0] + " [DIR FUENTE] [DIR DESTINO]")
	else:
		deleterto(argv[1], argv[2])

if __name__ == "__main__":
	main(sys.argv)
