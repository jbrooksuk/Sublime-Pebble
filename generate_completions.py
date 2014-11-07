#!/usr/bin/env python
# encoding: utf-8

"""
Generate sublime-completions file from Pebble header file.
Usage : python generate.py /path/to/pebble.h /path/to/pebble.sublime-completions
"""

import sys
import getopt
import re

def generate(header, output):
	pattern = r'^\w+\*?\s+\*?(\w+)\(([^\\/\(\)]*)\);'
	regex = re.compile(pattern, re.MULTILINE)

	f = open(header,'r')
	procs = [(i.group(1), i.group(2)) for i in regex.finditer(f.read())]
	f.close()

	content = ''
	content += '{\n'
	content += '\t"scope": "source",\n'
	content += '\t"completions": [\n'

	for i, proc in enumerate(procs):
		content += '\t\t{"trigger": "' + proc[0] + '", "contents": "' + proc[0] + '('

		varnames = proc[1].split(',')
		for j, varname in enumerate(varnames):
			varname = varname.split()[-1].split('*')[-1]
			content += '${' + str(j+1) + ':' + varname + '}'
			if j < len(varnames) - 1: content += ','

		content += ');"}'
		if i < len(procs) - 1: content += ','
		content += '\n'

	content += '\t]\n'
	content += '}\n'

	f = open(output,"w")
	f.write(content)
	f.close()


def main():
	# parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.error, msg:
		print msg
		print "for help use --help"
		sys.exit(2)
	# process options
	for o, a in opts:
		if o in ("-h", "--help"):
			print __doc__
			sys.exit(0)
	# process arguments
	if(len(args) == 2):
		generate(args[0], args[1])
	else:
		print "2 arguments are expected"
		print "for help use --help"
		sys.exit(2)

if __name__ == "__main__":
	sys.exit(main())
