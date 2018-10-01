#!/usr/bin/python

import csv
import os
import re
import pystache
import codecs
import glob
from shutil import copy


for file in glob.glob("*.csv"):
    parts = file.split(".")
    if not os.path.exists(parts[0]):
        cdir = os.makedirs(parts[0])
        print cdir
    copy("reg.mustache", parts[0])
    copy("gift.mustache", parts[0])
    copy("SockClub.png", parts[0])
    copy("TeamSignatures.png", parts[0])
    copy("buildletter.py", parts[0])
    copy(file, parts[0])
