#!/usr/bin/python

import csv
import os
import re
import pystache
import codecs
import glob
from shutil import copy

main_dir = os.getcwd()

for file in glob.glob("*.csv"):
    parts = file.split(".")
    if not os.path.exists(parts[0]):
        cdir = os.makedirs(parts[0])

    copy("reg.mustache", parts[0])
    copy("gift.mustache", parts[0])
    copy("SockClub.png", parts[0])
    copy("TeamSignatures.png", parts[0])
    copy("buildletter.py", parts[0])
    copy("AvenirLTStd-Black.otf", parts[0])
    copy("AvenirLTStd-Medium.otf", parts[0])
    copy("buildletter_max_csv.py", parts[0])
    copy("buildletter_06_23_2018.py", parts[0])
    copy(file, parts[0])
    os.chdir(parts[0])
    cmd = "python buildletter.py %s" % (file)
    os.system(cmd)
    os.chdir(main_dir)
