#!/usr/bin/python

import csv
import os
import re
import pystache
import codecs
import sys

names = csv.reader(open(sys.argv[1], 'rU'))
regtmpl = str(open("reg.mustache", "r").read())
gifttmpl = str(open("gift.mustache", "r").read())

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
        print(row)
        print(len(row))
        if str(row[4]) != 'null':
            toname = str(row[4])
        if str(row[21]) != 'null' and str(row[21]) != '#N/A' and str(row[21]) != '0':
            fromname = str(row[21])
        if str(row[22]) != 'null' and str(row[22]) != '#N/A' and str(row[22]) != '0':
            message = str(row[22])
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
            giftout = str(pystache.render(gifttmpl, context))
            f = open((filename + ".html"), 'w')
            f.write(giftout)
            f.close()
            # cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
            # print cmd
            # os.system(cmd)
            gc = gc + 1
        else:
            regout = str(pystache.render(regtmpl, context))
            f = open((filename + ".html"), 'w')
            f.write(regout)
            f.close()
            # cmd = "wkhtmltopdf %s.html %s.pdf" % (filename, filename)
            # print cmd
            # os.system(cmd)
    count = count + 1


cmd = "/usr/local/bin/wkhtmltopdf --enable-local-file-access *.html %s.pdf" % (
    csvname)
os.system(cmd)
