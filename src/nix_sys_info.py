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

def meminfo():
	res = subprocess.Popen(["cat","/proc/meminfo"],4096,stdout=subprocess.PIPE)
	field_values = [line.strip().split(":") for line in res.stdout.readlines()]
	ret = {}
	for fv in field_values:
		ret[fv[0].strip().lower()] = fv[1].strip()
	return ret

def process_info():
	res = subprocess.Popen(["ps","aux"],4096,stdout=subprocess.PIPE)
	lines = [l.strip() for l in res.stdout.readlines()]
	ret = []
	for line in lines:
		if line.startswith("USER"):
			continue
		line_map = {}
		keys=["user","pid","%cpu","%mem","vsz","rss","tty","stat","start","time","command0"]
		numeric_keys = ["pid","%cpu","%mem","vsz"]
		for (k,v) in zip(keys,line.split()):
			if not k in numeric_keys:
				line_map[k] = v 
			else:
				 line_map[k] = float(v)
		ret.append(line_map)	
	return ret

sys_info = {}
sys_info["disk_info"] = disk_info()
sys_info["mem_info"] = meminfo()
sys_info["process_info"] = process_info()
json_string = json.dumps(sys_info,indent=True)		
print(json_string)
	
