#! /usr/bin/env python3
###############################################################################
# Name: DataProcessor.py                                                      #
# Description: Functions that process data                                    #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################


def extract_fields(data, columns):
    """
    To retrieve an new list

    @param data: 2D array of tsv
    @param columns: The index of fields
    """
    # Converting to int from string for retrieving index
    try:
        for index, num in enumerate(columns):
            columns[index] = int(num)
    except ValueError:
        print('[-] ERROR-----Value in columns are not in')

    data_buf = []

    # To extract the data from the 2D array to Addr book
    for row in data:
        row_buf = list()
        for index, field in enumerate(columns):
            row_buf.append(row[field])
        data_buf.append(row_buf)

    return data_buf