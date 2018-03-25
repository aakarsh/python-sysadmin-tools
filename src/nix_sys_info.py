#!/usr/bin/env python

import subprocess
import json

def disk_info():
	res = subprocess.Popen(["df"],4096,stdout=subprocess.PIPE)
	lines = [l.strip() for l in res.stdout.readlines()]
	
	file_systems = []
	for line in lines:
		if line.startswith("Filesystem") or line.startswith("map"):
			continue
		fs = {}
		fields =  line.split()
		fs["file_system"],fs["blocks"],fs["used"],fs["available"] = fields[0],fields[1],fields[2],fields[3]
		fs["mounted"] = fields[-1]
		file_systems.append(fs)
	
	return file_systems


sys_info = {}
sys_info["disk_info"] = disk_info()

json_string = json.dumps(sys_info,indent=True)		
print(json_string)
	
