import csv
import sys

def update_row(count, dict):
    """
    Takes a dictionary and updates the row number
    """
    if dict[0]["start_row"] == None:
        dict[0]["start_row"] = count

    else:
        dict[0]["end_row"] = count


def parse_csv_to_dict(file_path):
    infile = csv.DictReader(open(file_path, "r"))
    list = []
    for row in infile:
        list.append(row)
    return list


def parse_dict(dict_list):
    """
    takes a list of dictionaries and sorts them into lists by order type
    """
    FL_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FL_INTL[0]["size_code"] = 'FL'
    FL_INTL[0]["country_code"] = 'INTL'
    FL_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FL_US[0]["size_code"] = 'FL'
    FL_US[0]["country_code"] = 'US'
    FM_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FM_INTL[0]["size_code"] = 'FM'
    FM_INTL[0]["country_code"] = 'INTL'
    FM_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FM_US[0]["size_code"] = 'FM'
    FM_US[0]["country_code"] = 'US'
    FS_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FS_INTL[0]["size_code"] = 'FS'
    FS_INTL[0]["country_code"] = 'INTL'
    FS_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    FS_US[0]["size_code"] = 'FS'
    FS_US[0]["country_code"] = 'US'
    ML_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    ML_INTL[0]["size_code"] = 'ML'
    ML_INTL[0]["country_code"] = 'INTL'
    ML_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    ML_US[0]["size_code"] = 'ML'
    ML_US[0]["country_code"] = 'US'
    MM_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    MM_INTL[0]["size_code"] = 'MM'
    MM_INTL[0]["country_code"] = 'INTL'
    MM_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    MM_US[0]["size_code"] = 'MM'
    MM_US[0]["country_code"] = 'US'
    MS_INTL = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    MS_INTL[0]["size_code"] = 'MS'
    MS_INTL[0]["country_code"] = 'INTL'
    MS_US = [dict.fromkeys(["start_row", "end_row", "size_code", "country_code"])]
    MS_US[0]["size_code"] = 'MS'
    MS_US[0]["country_code"] = 'US'

    row_num = 0
    for row in dict_list:
        if row["Country (iso)"] == "US":
            if (
                row["Sub type"] == "adult_female"
                or row["Sub type"] == "NA"
                or row["Sub type"] == ""
                or row["Sub type"] == "kid_female"
            ):
                if row["Size"] == "small" or row["Size"] == "youth":
                    FS_US.append(row)
                    update_row(row_num, FS_US)
                elif row["Size"] == "large":
                    FL_US.append(row)
                    update_row(row_num, FL_US)
                else:
                    FM_US.append(row)
                    update_row(row_num, FM_US)
            else:
                if row["Size"] == "small" or row["Size"] == "youth":
                    MS_US.append(row)
                    update_row(row_num, MS_US)
                elif row["Size"] == "large":
                    ML_US.append(row)
                    update_row(row_num, ML_US)
                else:
                    MM_US.append(row)
                    update_row(row_num, MM_US)

        else:
            if (
                row["Sub type"] == "adult_female"
                or row["Sub type"] == "NA"
                or row["Sub type"] == ""
                or row["Sub type"] == "kid_female"
            ):
                if row["Size"] == "small" or row["Size"] == "youth":
                    FS_INTL.append(row)
                    update_row(row_num, FS_INTL)
                elif row["Size"] == "large":
                    FL_INTL.append(row)
                    update_row(row_num, FL_INTL)
                else:
                    FM_INTL.append(row)
                    update_row(row_num, FM_INTL)
            else:
                if row["Size"] == "small" or row["Size"] == "youth":
                    MS_INTL.append(row)
                    update_row(row_num, MS_INTL)
                elif row["Size"] == "large":
                    ML_INTL.append(row)
                    update_row(row_num, ML_INTL)
                else:
                    MM_INTL.append(row)
                    update_row(row_num, MM_INTL)
        row_num += 1

    return (
        FL_INTL,
        FL_US,
        FM_INTL,
        FM_US,
        FS_INTL,
        FS_US,
        ML_INTL,
        ML_US,
        MM_INTL,
        MM_US,
        MS_INTL,
        MS_US,
    )


def make_csv(dict_list):
    """
    Takes a list of dictionaries and writes them to a CSV file
    """

    column_names = dict_list[1].keys()
    csv_name = "{size_code}_{first_row}_{last_row}_{country_code}.csv".format(
        size_code=dict_list[0]["size_code"],
        first_row=dict_list[0]["start_row"],
        last_row=dict_list[0]["end_row"],
        country_code=dict_list[0]["country_code"],
    )
    print(csv_name)
    with open(csv_name, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=column_names)
        writer.writeheader()
        for row in dict_list[1:]:
            writer.writerow(row)

if __name__ == "__main__":
    csv_dict = parse_csv_to_dict(sys.argv[1])
    FL_INTL, FL_US, FM_INTL, FM_US, FS_INTL, FS_US, ML_INTL, ML_US, MM_INTL, MM_US, MS_INTL, MS_US = parse_dict(csv_dict)
    make_csv(FL_INTL)
    make_csv(FL_US)
    make_csv(FM_INTL)
    make_csv(FM_US)
    make_csv(FS_INTL)
    make_csv(FS_US)
    make_csv(ML_INTL)
    make_csv(ML_US)
    make_csv(MM_INTL)
    make_csv(MM_US)
    make_csv(MS_INTL)
    make_csv(MS_US)
