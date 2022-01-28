#!/usr/bin/python

import csv
from email.policy import default
import os
import pystache
import sys


def remove_non_ascii(text):
    return text.encode("ascii", "ignore").decode()

def build_letters(file = None): 

    if file is None: 
        names = csv.reader(open(sys.argv[1], "rU"))
        csvname = sys.argv[1].split(".")[0]
        folder_name = file.replace(".csv", "")
    else: 
        names = csv.reader(open("csv/" + file, "rU"))
        csvname = file.split(".")[0]

    regtmpl = str(open("reg.mustache", "r").read())
    gifttmpl = str(open("gift.mustache", "r").read())

    count = 0
    gc = 0
    stop = 0

    if not os.path.exists("generated_pdfs/"):
        os.makedirs("generated_pdfs/")

    if not os.path.exists("htmls/"): 
        os.makedirs("htmls/")

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

def merge_pdfs(pdf_name): 
    from PyPDF2 import PdfFileMerger, PdfFileReader
    merger = PdfFileMerger()
    for file in os.listdir("generated_pdfs/"):
        if file.endswith(".pdf") and os.path.exists("generated_pdfs/" + file):
            input = PdfFileReader(open("generated_pdfs/" + file, "rb"))
            merger.append(input, import_bookmarks=False)
    if not os.path.exists("merged_pdfs/"):
        os.makedirs("merged_pdfs/")
    merger.write(open("merged_pdfs/" + pdf_name + ".pdf", "wb"))
    print("Merged PDFs at " + pdf_name + ".pdf")
    remove_blank_pages(pdf_name)

def remove_blank_pages(pdf_name):
    from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
    import pdfplumber
    pdfReader = PdfFileReader(open("merged_pdfs/" + pdf_name + ".pdf", "rb"))
    PdfFileWriter = PdfFileWriter()
    with pdfplumber.open("merged_pdfs/" + pdf_name + ".pdf") as plumber:
        for page in range(pdfReader.getNumPages()):
            if len(plumber.pages[page].chars) > 0: 
                PdfFileWriter.addPage(pdfReader.getPage(page))
                print('added page')
    if not os.path.exists("final_pdfs/"):
        os.makedirs("final_pdfs/")
    PdfFileWriter.write(open("final_pdfs/" + pdf_name + ".pdf", "wb"))
    print("Removed blank pages at " + pdf_name + ".pdf")

def remove_pdfs(): 
    for file in os.listdir("generated_pdfs/"):
        if file.endswith(".pdf") and file.startswith("0"):
            os.remove("generated_pdfs/" + file)

    for file in os.listdir("htmls/"):
        if file.endswith(".html") and file.startswith("0"):
            os.remove("htmls/" + file)

if __name__ == "__main__":
    import argparse
    from split_csv import split 
    argparser = argparse.ArgumentParser(description="Build letters")
    argparser.add_argument("--filepath", type=str, help="Path to csv file")
    args = argparser.parse_args()
    if args.filepath:
        split(args.filepath)
        for file in os.listdir("csv/"):
            if file.endswith(".csv"):
                build_letters(file)
                merge_pdfs(file.replace(".csv", ""))
                remove_pdfs()

    else:
       "Didn't get a csv file path. Use --filepath to specify a csv file. Ex: 'python buildletter.py --name=example.csv'" 