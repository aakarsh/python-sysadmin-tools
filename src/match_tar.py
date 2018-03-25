#!/usr/bin/env python

import subprocess
import os
import re
import argparse
import time

tar_dir = "/tmp"
tar_file_name = "matching"

if __name__ == "__main__":
	usage ="tar-matching <dir> <pattern> [-o file-name]" 
	parser = argparse.ArgumentParser(usage = usage, 
					 description="Parse files matching pattern in directory")
	parser.add_argument(dest="directory", type=str )
	parser.add_argument(dest="patterns",  type=str, nargs="+")
	parser.add_argument("-o",dest="out_file",  type=str, default=tar_dir+"/"+tar_file_name)
	parser.add_argument("-t",dest="timestamp",  action="store_const",const=True,default=False)

	args = parser.parse_args()

	if not args.directory or not args.patterns:
		args.print_help()
		exit(1)

	if not os.path.isdir(str(args.directory)):
		print("%s is not a direcotry",args.directory)
		args.print_help()
		exit(1)

	def matches_patterns(patterns, file):
		for p in patterns:
			if re.match(p,file):
				return True
		return False

	matching_files = []
	for file in os.listdir(args.directory):
		if matches_patterns(args.patterns,file):
			matching_files.append(file)

	if args.timestamp:
		args.out_file+=time.strftime("_%Y_%m_%d_%H_%M_%S",time.gmtime())

	cmd = ["tar", "cvzf",args.out_file+".tar.gz"] 
	cmd.extend(matching_files)
	subprocess.call(cmd)

