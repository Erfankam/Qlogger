#!/usr/bin/python

import os, sys, inspect, traceback

def a(args = None):
	print 'inside a'
	b()

def b(args = None):
	print 'inside b'
	c()

def c(args = None):
	print 'inside c'
	exc_type, exc_value, exc_traceback = sys.exc_info()
	print exc_traceback
	traceback.print_stack()
	print traceback.extract_stack()
	print ">>>>>>>>>>>>>>>>>>>"
	print inspect.stack()
	#traceback.print_tb(sys.stdout)

if __name__ == "__main__":
	a()
