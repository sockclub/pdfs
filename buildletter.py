#!/usr/bin/python
import csv
from doctest import master
from email.policy import default
import os
import pystache
import sys
from split_csv import parse_csv_to_dict
import inflection


def remove_non_ascii(text):
    return text.encode("ascii", "ignore").decode()


def builder(file=None):
    csv_dict = parse_csv_to_dict(file)
    regtmpl = str(open("reg.mustache", "r").read())
    gifttmpl = str(open("gift.mustache", "r").read())
    if not os.path.exists("generated_pdfs/"):
        os.makedirs("generated_pdfs/")
    if not os.path.exists("htmls/"):
        os.makedirs("htmls/")

    for row in csv_dict:
        to_name = row["Recipient name"]
        from_name = row["Fromname"]
        message = row["Message"]

        # map the size to the correct size code
        if "small" in row["Size"]:
            size = "S"
        elif "large" in row["Size"]:
            size = "L"
        elif "youth" in row["Size"]:
            size = "Y"
        elif "medium" in row["Size"]:
            size = "M"
        elif "Medium" in row["Size"]:
            size = "M"
        else:
            raise Exception("Invalid size for recipient " + row["Recipient name"])

        # map the style/gender
        if row["Sub type"] == "adult_female":
            gender = "F"
        elif row["Sub type"] == "kid_female":
            gender = "F"
        elif row["Sub type"] == "adult_male":
            gender = "M"
        elif row["Sub type"] == "kid_male":
            gender = "M"

        # if the message is blank, generate regular html doc with no gift message
        html_str = str(
            pystache.render(
                regtmpl if message == "" else gifttmpl,
                {
                    "ToName": to_name,
                    "FromName": from_name,
                    "MESSAGE": message,
                    "Size": size,
                    "Gender": gender,
                },
            )
        )
        master_file_name = file.replace(".csv", "").replace("csv/", "")
        print(master_file_name)
        append_html_string_to_pdf(
            html_str, inflection.parameterize(to_name), master_file_name
        )


def append_html_string_to_pdf(html_str, temp_file_name, master_file_name="master"):
    from PyPDF2 import PdfFileMerger, PdfFileReader

    # write the html to a file
    f = open(("htmls/" + temp_file_name + ".html"), "w")
    f.write(html_str)
    f.close()

    # if the master pdf doesn't exist yet, create it and return
    if not os.path.exists("merged_pdfs/" + master_file_name + ".pdf"):
        os.system(
            "/usr/local/bin/wkhtmltopdf --enable-local-file-access htmls/"
            + temp_file_name
            + ".html merged_pdfs/"
            + master_file_name
            + ".pdf"
        )
        return

    # if the master pdf exists, make a new pdf from the html
    os.system(
        "/usr/local/bin/wkhtmltopdf --enable-local-file-access htmls/"
        + temp_file_name
        + ".html generated_pdfs/"
        + temp_file_name
        + ".pdf"
    )

    # merge the new pdf with the master pdf
    merger = PdfFileMerger()
    merger.append(
        PdfFileReader(open("merged_pdfs/" + master_file_name + ".pdf", "rb")),
        import_bookmarks=False,
    )
    merger.append(
        PdfFileReader(open("generated_pdfs/" + temp_file_name + ".pdf", "rb")),
        import_bookmarks=False,
    )
    merger.write(open("merged_pdfs/" + master_file_name + ".pdf", "wb"))
    print("Appended " + temp_file_name + " to merged_pdfs/" + master_file_name + ".pdf")


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
    from PyPDF2 import PdfFileReader, PdfFileWriter
    import pdfplumber

    pdfReader = PdfFileReader(open("merged_pdfs/" + pdf_name + ".pdf", "rb"))
    PdfFileWriter = PdfFileWriter()
    with pdfplumber.open("merged_pdfs/" + pdf_name + ".pdf") as plumber:
        for page in range(pdfReader.getNumPages()):
            if len(plumber.pages[page].chars) > 0:
                PdfFileWriter.addPage(pdfReader.getPage(page))
                print("added page")
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
                builder("csv/" + file)
                remove_blank_pages(file.replace(".csv", ""))
                remove_pdfs()

    else:
        "Didn't get a csv file path. Use --filepath to specify a csv file. Ex: 'python buildletter.py --name=example.csv'"
