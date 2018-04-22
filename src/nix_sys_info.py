#!/usr/bin/env python

import subprocess
import json

def run(cmd,args=[]):
	"""Run a command and pipe its output"""
	if not cmd: ValueError("Empty command")
	cmd_args = [cmd]
	if args: cmd_args += args
	return subprocess.Popen(cmd_args,4096,stdout=subprocess.PIPE)
	
def disk_info():
	"""Parses fields of disk information as a map on linux and returns 
	it as a map."""
	lines = [l.strip() for l in run("df").stdout.readlines()]
	file_systems = []
	for line in lines:
		if line.startswith("Filesystem") or line.startswith("map"):
			continue
		fs = {}
		fields =  line.split()
		field_mapping = {
			"file_system" : 0,
			"blocks"      : 1,
			"used"	      : 2,
			"available"   : 3,
			"mounted"     : -1 }

		for field_key in field_mapping.keys():
			fs[field_key] = fields[field_mapping[field_key]]

		file_systems.append(fs)
	return file_systems

def mem_info():
	"""Parses fields in the memory info file of linux and 
	returns it as a map."""
	field_values = [line.strip().split(":") 
				for line in run("cat",["/proc/meminfo"]).stdout.readlines()]
	ret = {}
	for fv in field_values:
		ret[fv[0].strip().lower()] = fv[1].strip()
	return ret

def process_info():
	"""Parses fields in the process info and returns it as a map."""
	lines = [l.strip() for l in run("ps",["aux"]).stdout.readlines()]
	ret = []
	for line in lines:
		if line.startswith("USER"):
			continue
		line_map = {}

		keys = ["user","pid","%cpu","%mem","vsz",
			"rss","tty","stat","start","time",
			"command0"]

		numeric_keys = ["pid","%cpu","%mem","vsz"]

		for (k,v) in zip(keys,line.split()):
			if not k in numeric_keys:
				line_map[k] = v 
			else:
				 line_map[k] = float(v)

		ret.append(line_map)	
	return ret

sys_info = {
	"disk_info" 	: disk_info(),
	"mem_info"  	: mem_info (),
	"process_info" 	: process_info()
}

print(json.dumps(sys_info,indent=True))

