#!/usr/bin/python

import csv
import os
import re
import pystache
import codecs
import sys

names = csv.reader(open(sys.argv[1], 'rU'))
regtmpl = unicode(open("reg.mustache", "r").read().decode('utf-8'))
gifttmpl = unicode(open("gift.mustache", "r").read().decode('utf-8'))

count = 0
gc = 0
stop = 0

csvname = sys.argv[1].split(".")[0]

for row in names:
    if count > stop:
        toname = ""
        fromname = ""
        message = ""
        size = "M"
        gender = "M"
        print row
        print len(row)
        if unicode(row[4], 'utf-8', errors='ignore') != 'null':
            toname = unicode(row[4], 'utf-8', errors='ignore')
        if unicode(row[16], 'utf-8', errors='ignore') != 'null':
            fromname = unicode(row[16], 'utf-8', errors='ignore')
        if unicode(row[17], 'utf-8', errors='ignore') != 'null':
            message = unicode(row[17], 'utf-8', errors='ignore')
        if row[18] == 'small':
            size = "S"
        if row[18] == 'large':
            size = "L"
        if row[18] == 'youth':
            size = "Y"

        if row[19] == "adult_female":
            gender = "F"
        if row[19] == "kid_female":
            gender = "F"

        filename = "{0:05d}".format(count)
        context = {'ToName': toname, 'FromName': fromname,
                   'MESSAGE': message, 'Size': size, 'Gender': gender}
        if message:
            giftout = pystache.render(gifttmpl, context).encode('utf-8')
            f = open((filename + ".html"), 'w')
            f.write(giftout)
            f.close()
            # cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
            # print cmd
            # os.system(cmd)
            gc = gc + 1
        else:
            regout = pystache.render(regtmpl, context).encode('utf-8')
            f = open((filename + ".html"), 'w')
            f.write(regout)
            f.close()
            # cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
            # print cmd
            # os.system(cmd)
    count = count + 1


cmd = "wkhtmltopdf --zoom 3.5 *.html %s.pdf" % (csvname)
os.system(cmd)
