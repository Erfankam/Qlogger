#!/usr/bin/python

from ekloggger import *

d = [6, 6, [{'Erfan':'Erfan', 'Qazal':'Qazal'}, {'Ali':'Mohammmad', 'Erfan':'Mahdi'}, [6,7,8,9,10, {1124:[1,4,1,2,4,3]}], 3 , 5, 6]]
d1 = [6, 6, {'Erfan':'Erfan', 'Qazal':'Qazal'}, {'Ali':'Mohammmad', 'Erfan':'Mahdi'}, 3 , 5, 6]
d={'Erfan':'Erfan', 'Qazal':'Qazal'} 
d1={'Erfan':'Erfan', 'Qazal':'Qazal'}
ekl = Qlogger("Qazal logger module test suite and its argument")
ekh = FileHandler('f.log', '', ' | date time: must affect>>> %dt\n | platform name: %pn \n | module name: %mn \n | class name: %cn\n \
| log name: %ln \n | log object: %lo \n | function name: %fn\n | document string: %ds\n | platform name: %pn \n | log type: %lt\n \
| standard input: %si\n | standard output: %so \n | standard error: %se\n | thread id: %ti\n | process id: %pi\n | user log: %ul\n \
| os version: %ov\n | file address: %fa| os arch: %oa \n | os family: %of\n | os name: %on\n | host name: %hn\n >>> test: %dt%%%%dt  %ti%ti%ti')
qkl.setLogLevel(3)
qkl.addHandler(ekh)

class a():
	def a1(self):
		print "this is a test"
		qkl.Qlog('This what i mean', None, 4)

aobj = a()
aobj.a1()
qkl.Qlog("je suis pret  \n %q \n ################################# \nand its args is \n %q \n", (d1, d))
exit()
