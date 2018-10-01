#!/usr/bin/python

import csv
import os
import re
import sys
import pystache
import codecs
import glob
from shutil import copy

parts = sys.argv[1].split(".")
# parts = file.split(".")
if not os.path.exists(parts[0]):
    cdir = os.makedirs(parts[0])
    print cdir
copy("reg.mustache", parts[0])
copy("gift.mustache", parts[0])
copy("SockClub.png", parts[0])
copy("TeamSignatures.png", parts[0])
copy("buildletter.py", parts[0])
copy("buildletter_max_csv.py", parts[0])
copy(sys.argv[1], parts[0])
