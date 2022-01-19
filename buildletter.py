#!/usr/bin/python

import csv
import os
import pystache
import sys


names = csv.reader(open(sys.argv[1], "rU"))
regtmpl = str(open("reg.mustache", "r").read())
gifttmpl = str(open("gift.mustache", "r").read())

count = 0
gc = 0
stop = 0

csvname = sys.argv[1].split(".")[0]


def remove_non_ascii(text):
    return text.encode("ascii", "ignore").decode()


if not os.path.exists("generated_pdfs/"):
    os.makedirs("generated_pdfs/")

for row in names:
    if count > stop:
        toname = ""
        fromname = ""
        message = ""
        size = "M"
        gender = "M"
        print(row)
        print(len(row))
        if str(row[4]) != "null":
            toname = remove_non_ascii(str(row[4]))
        if str(row[21]) != "null" and str(row[21]) != "#N/A" and str(row[21]) != "0":
            fromname = remove_non_ascii(str(row[21]))
        if str(row[22]) != "null" and str(row[22]) != "#N/A" and str(row[22]) != "0":
            message = remove_non_ascii(str(row[22]))
        if row[18] == "small":
            size = "S"
        if row[18] == "large":
            size = "L"
        if row[18] == "youth":
            size = "Y"

        if row[19] == "adult_female":
            gender = "F"
        if row[19] == "kid_female":
            gender = "F"

        filename = "{0:05d}".format(count)
        context = {
            "ToName": toname,
            "FromName": fromname,
            "MESSAGE": message,
            "Size": size,
            "Gender": gender,
        }
        if message:
            giftout = str(pystache.render(gifttmpl, context))
            f = open(("htmls/" + filename + ".html"), "w")
            f.write(giftout)
            f.close()
            cmd = (
                "/usr/local/bin/wkhtmltopdf --enable-local-file-access htmls/"
                + filename
                + ".html generated_pdfs/"
                + filename
                + ".pdf"
            )
            os.system(cmd)
        else:
            regout = str(pystache.render(regtmpl, context))
            f = open(("htmls/" + filename + ".html"), "w")
            f.write(regout)
            f.close()
            cmd = (
                "/usr/local/bin/wkhtmltopdf --enable-local-file-access htmls/"
                + filename
                + ".html generated_pdfs/"
                + filename
                + ".pdf"
            )
            os.system(cmd)
    count = count + 1
