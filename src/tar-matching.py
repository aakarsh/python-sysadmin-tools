#!/usr/bin/python

import subprocess
import os
import re


if __name__ == "__main__":
	matching_files = []
	for file in os.listdir("."):
		if re.match(".*",file):
			matching_files.append(file)

	cmd = ["tar", "vfzc","files.tar.gz"] 
	cmd.extend(matching_files)

	subprocess.call(cmd)


