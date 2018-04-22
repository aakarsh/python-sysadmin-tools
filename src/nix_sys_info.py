#!/usr/bin/env python
import subprocess
import json
class sys_info:

	def __init__(self):
		pass

	def disk_info(self):
		"""Parses fields of disk information as a map on linux and returns 
		it as a map."""
		output_lines = sys_info._run("df").stdout.readlines()
		lines = [l.strip() for l in output_lines]
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


	def mem_info(self):
		"""Parses fields in the memory info file of linux and 
		returns it as a map."""
		output_lines = sys_info._run("cat","/proc/meminfo").stdout.readlines()  
		field_values = [line.strip().split(":") for line in output_lines]
		ret = {}
		for fv in field_values:
			ret[fv[0].strip().lower()] = fv[1].strip()
		return ret

	def process_info(self):
		"""Parses fields in the process info and returns it as a map."""
		output_lines = sys_info._run("ps","aux").stdout.readlines()
		lines = [l.strip() for l in output_lines]
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

	def get_sys_info(self):
		return {"disk_info" 	: self.disk_info(),
			"mem_info"  	: self.mem_info (),
			"process_info" 	: self.process_info()}

	def json(self):
		return json.dumps(self.get_sys_info(),indent=True)

	@classmethod
	def _run(cls,cmd,*args):
		"""Run a command and pipe its output"""
		if not cmd: ValueError("Empty command")
		cmd_args = [cmd]
		if args: cmd_args += args
		return subprocess.Popen(cmd_args,4096,stdout=subprocess.PIPE)
		
if __name__ == "__main__":
	print(sys_info().json())
