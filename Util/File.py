#! /usr/bin/env python3
###############################################################################
# Name: file.py                                                               #
# Description: files related functions                                        #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

import csv

def read_csv_to_list(path: str, remove_label=True):
    """
    read_csv_to_list(path: str, remove_label=True)
    @param path: the path to the csv file
    @param remove_label: remove the column header 

    Read the whole csv file into memory.
    This will return a 2D list.
    """
    if remove_label is True:
        LABEL = 1
    else:
        LABEL = 0

    try:
        with open(path, 'r') as fp:
            csvdata = csv.reader(fp, delimiter='\t', quotechar='\'')
            return list(csvdata)[LABEL:]
    except FileNotFoundError:
        print('[-] ERROR: {}----FILE NOT FOUND'.format(path))
        # if file not found, return empty
        return list()


def read_txt(path: str):
    """
    read_txt(path: str)
    @param path: the path to the txt file

    Read text to str
    """
    with open(path, 'r') as fp:
        buf = fp.read()
    return buf