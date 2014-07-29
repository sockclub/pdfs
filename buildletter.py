#!/usr/bin/python

import csv, os, re
import pystache

names = csv.reader(open('Round2.csv'))
regtmpl = unicode(open("reg.mustache","r").read())
gifttmpl = unicode(open("gift.mustache","r").read())

count = 0
gc = 0
stop = 0

for row in names:
	if count > stop:
		toname = ""
		fromname = ""
		message = ""
		size = "M"
		if str(row[4]) != 'null':
			toname = str(row[4])
		if str(row[13]) != 'null' and str(row[13]) != '#N/A' and str(row[13]) != '0':
			fromname = str(row[13])
		if str(row[14]) != 'null' and str(row[14]) != '#N/A' and str(row[14]) != '0':
			message = str(row[14])
		if row[12] == 'small':
			size = "S"
		if row[12] == 'large':
			size = "L"	

		filename = "{0:05d}".format(count)
		context = {'ToName' : toname, 'FromName' : fromname, 'MESSAGE' : message, 'Size': size}
		if message:
			giftout = pystache.render(gifttmpl,context)
			f = open((filename+".html"), 'w')
			f.write(giftout)
			f.close()
			cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
			print cmd
			os.system(cmd)
			gc = gc + 1
		else:
			regout = pystache.render(regtmpl,context)
			f = open((filename+".html"), 'w')
			f.write(regout)
			f.close()
			cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
			print cmd
			os.system(cmd)
		print gc
	count = count + 1