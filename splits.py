#!/usr/bin/python
import csv
import os
import pandas
from pandas import ExcelWriter
from itertools import tee
import math
import sys

# input - df: a Dataframe, chunkSize: the chunk size
# output - a list of DataFrame
# purpose - splits the DataFrame into smaller of max size chunkSize (last
# is smaller)
# def chunkDataFrame(df, chunkSize=500, start_index=1):
#     listOfDf = list()
#     numberChunks = len(df) // chunkSize + 1
#     for i in range(numberChunks):
#         listOfDf.append(df[i * chunkSize:(i + 1) * chunkSize])
#     return listOfDf
def roundup(x):
    return int(math.ceil(x / 500.0)) * 500


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def chunkDataFrame(df, begin_fstr, end_fstr, chunkSize=500, start_index=0):
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        chunk_500 = df[i * chunkSize : (i + 1) * chunkSize]
        display_index = start_index
        start_index = start_index + len(chunk_500)
        fstr = (
            begin_fstr
            + "_"
            + str(display_index)
            + "_"
            + str(start_index)
            + "_"
            + end_fstr
            + ".csv"
        )
        chunk_500.to_csv(fstr, index=False, sep=",")
    return start_index


def oneChunk(df, begin_fstr, end_fstr, chunkSize, start_index):
    out = df[:chunkSize]
    end_index = start_index + chunkSize
    fstr = (
        begin_fstr
        + "_"
        + str(start_index)
        + "_"
        + str(end_index)
        + "_"
        + end_fstr
        + ".csv"
    )
    out.to_csv(fstr, index=False, sep=",")
    rest = df[(chunkSize + 1) :]
    return rest


def indices(start, length):
    indices_list = list()
    len_indices_list = length // 500 + 1
    first_chunk = 500 - start % 500
    second_index = start + first_chunk
    indices_list.append(start)
    if length > 500:
        indices_list.append(second_index)
    for i in range(len_indices_list - 2):
        indices_list.append((i + 1) * 500 + second_index)
    indices_list.append(start + length)
    return indices_list


# def index_array(start, length):
#     ilist = list()
#     ilist.append(start)
#     if ((start % 500 != 0) and (start > 500)):
#         after_start = roundup(start)
#         ilist.append(after_start)
#     while last_in < start + length
#         if()
#         ilist
def chunkOnIndices(df, start_index, begin_fstr, end_fstr):
    indxs = indices(start_index, len(df))
    print(indxs)
    for pairs in pairwise(indxs):
        chunk = df[(pairs[0] - start_index) : (pairs[1] - start_index)]
        first_display_index = pairs[0] + 1
        fstr = (
            begin_fstr
            + "_"
            + str(first_display_index)
            + "_"
            + str(pairs[1])
            + end_fstr
            + ".xlsx"
        )
        writer = ExcelWriter(fstr)
        chunk.to_excel(writer, index=False, sheet_name="Sheet1")
        writer.save()
        # chunk.to_csv(fstr, index=False, sep=',')


def changeencode(data, cols):
    for col in cols:
        print(data[col].dtype)
        if data[col].dtype == "object":
            print("transcoding\n")
            data[col] = data[col].str.decode("iso-8859-1").str.encode("utf-8")
    return data


csv = pandas.read_csv(sys.argv[1], sep=",", skipinitialspace=True, dtype=object)
csv = changeencode(csv, list(csv))
print("Sizes:\n")
print(csv.groupby("Size").groups.keys())
print("\n")
print("Sub Types:\n")
print(csv.groupby("Sub type").groups.keys())
print("\n")
print("Countries:\n")
print(csv.groupby("Country (iso)").groups.keys())
print(len(csv.groupby("Country (iso)").groups.keys()))
print("\n")
female = csv[((csv["Sub type"] == "adult_female") | (csv["Sub type"] == "kid_female"))]
male = csv[~((csv["Sub type"] == "adult_female") | (csv["Sub type"] == "kid_female"))]
male_medium = male[
    (male["Size"] == "medium")
    | (male["Size"] == "Medium")
    | (male["Size"] == "medium ")
]
male_medium_intl = male_medium[
    ~((male_medium["Country (iso)"] == "US") | (male_medium["Country (iso)"] == "Us"))
]
male_medium_us = male_medium[
    ((male_medium["Country (iso)"] == "US") | (male_medium["Country (iso)"] == "Us"))
]
male_large = male[
    (male["Size"] == "large") | (male["Size"] == "Large") | (male["Size"] == "LARGE")
]
male_large_intl = male_large[
    ~((male_large["Country (iso)"] == "US") | (male_large["Country (iso)"] == "Us"))
]
male_large_us = male_large[
    ((male_large["Country (iso)"] == "US") | (male_large["Country (iso)"] == "Us"))
]
male_small = male[(male["Size"] == "Small") | (male["Size"] == "small")]
male_small_intl = male_small[
    ~((male_small["Country (iso)"] == "US") | (male_small["Country (iso)"] == "Us"))
]
male_small_us = male_small[
    ((male_small["Country (iso)"] == "US") | (male_small["Country (iso)"] == "Us"))
]
male_small_ordered = pandas.concat(
    [male_small_intl.sort_values(by="Country (iso)"), male_small_us]
)
print("Male Small Check:\n")
print(len(male_small.index) == len(male_small_ordered.index))
print("\n")
male_youth = male[(male["Size"] == "youth")]
male_youth_intl = male_youth[
    ~((male_youth["Country (iso)"] == "US") | (male_youth["Country (iso)"] == "Us"))
]
male_youth_us = male_youth[
    ((male_youth["Country (iso)"] == "US") | (male_youth["Country (iso)"] == "Us"))
]
male_youth_ordered = pandas.concat(
    [male_youth_intl.sort_values(by="Country (iso)"), male_youth_us]
)
print("Male Youth Check:\n")
print(len(male_youth.index) == len(male_youth_ordered.index))
print("\n")
female_youth = female[(female["Size"] == "youth")]
female_youth_intl = female_youth[
    ~((female_youth["Country (iso)"] == "US") | (female_youth["Country (iso)"] == "Us"))
]
female_youth_us = female_youth[
    ((female_youth["Country (iso)"] == "US") | (female_youth["Country (iso)"] == "Us"))
]
female_youth_ordered = pandas.concat(
    [female_youth_intl.sort_values(by="Country (iso)"), female_youth_us]
)
print("Female Youth Check:\n")
print(len(female_youth.index) == len(female_youth_ordered.index))
print("\n")
female_small = female[(female["Size"] == "small") | (female["Size"] == "Small")]
female_small_intl = female_small[
    ~((female_small["Country (iso)"] == "US") | (female_small["Country (iso)"] == "Us"))
]
female_small_us = female_small[
    ((female_small["Country (iso)"] == "US") | (female_small["Country (iso)"] == "Us"))
]
female_medium = female[
    (female["Size"] == "medium")
    | (female["Size"] == "Medium")
    | (female["Size"] == "medium ")
]
female_medium_intl = female_medium[
    ~(
        (female_medium["Country (iso)"] == "US")
        | (female_medium["Country (iso)"] == "Us")
    )
]
female_medium_us = female_medium[
    (
        (female_medium["Country (iso)"] == "US")
        | (female_medium["Country (iso)"] == "Us")
    )
]
female_medium_ordered = pandas.concat(
    [female_medium_intl.sort_values(by="Country (iso)"), female_medium_us]
)
print("Female Medium Check:\n")
print(len(female_medium.index) == len(female_medium_ordered.index))
print("\n")
female_large = female[
    (female["Size"] == "large")
    | (female["Size"] == "Large")
    | (female["Size"] == "LARGE")
]
female_large_intl = female_large[
    ~((female_large["Country (iso)"] == "US") | (female_large["Country (iso)"] == "Us"))
]
female_large_us = female_large[
    ((female_large["Country (iso)"] == "US") | (female_large["Country (iso)"] == "Us"))
]
female_large_ordered = pandas.concat(
    [female_large_intl.sort_values(by="Country (iso)"), female_large_us]
)
print("Female Large Check:\n")
print(len(female_large.index) == len(female_large_ordered.index))
print("\n")
# csv[(csv["Country (ISO)"] == "Us")]
# idx1 = indices(0, len(male_medium_intl))
# idx2 = indices(len(male_medium_intl), len(male_medium_us))
chunkOnIndices(male_youth_intl, 0, "MY", "_INTL")
chunkOnIndices(male_youth_us, len(male_youth_intl), "MY", "_US")
chunkOnIndices(male_small_intl, 0, "MS", "_INTL")
chunkOnIndices(male_small_us, len(male_small_intl), "MS", "_US")
male_medium_intl = male_medium_intl.sort_values(by="Country (iso)")
chunkOnIndices(male_medium_intl, 0, "MM", "_INTL")
chunkOnIndices(male_medium_us, len(male_medium_intl), "MM", "_US")
chunkOnIndices(male_large_intl, 0, "ML", "_INTL")
chunkOnIndices(male_large_us, len(male_large_intl), "ML", "_US")
chunkOnIndices(female_youth_intl, 0, "FY", "_INTL")
chunkOnIndices(female_youth_us, len(female_youth_intl), "FY", "_US")
chunkOnIndices(female_small_intl, 0, "FS", "_INTL")
chunkOnIndices(female_small_us, len(female_small_intl), "FS", "_US")
chunkOnIndices(female_medium_intl, 0, "FM", "_INTL")
chunkOnIndices(female_medium_us, len(female_medium_intl), "FM", "_US")
chunkOnIndices(female_large_intl, 0, "FL", "_INTL")
chunkOnIndices(female_large_us, len(female_large_intl), "FL", "_US")
# end_count = chunkDataFrame(male_medium_intl, "MM", "INTL")
# smallChunkSize = 500 - end_count % 500
# rest_male_medium_us = oneChunk(
#     male_medium_us, "MM", "US", smallChunkSize, end_count)
# last_value = chunkDataFrame(rest_male_medium_us, "MM", "US", 500, end_count)
