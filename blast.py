#! /usr/bin/env python3
###############################################################################
# Name: Blast.py                                                              #
# Description: Blaster                                                        #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

from EmailBlaster.Mail import Mail
from EmailBlaster.EmailBlaster import EmailBlaster
from Util import File
from Util import DataProcessor as dp
import argparse
import configparser

def get_sample(send_to, template, column_data):
    """
    Get the mail object to be returned as a __str__
    Retrieve the first

    @param send_to: the list that holds the sendee
    @param template: email template
    @param column_data: specify columns

    return void
    """
    mail = Mail(send_to[0], "SAMPLE", template, column_data[0])
    print(str(mail))


def main():
    """
    The Main method
    """
    config = configparser.ConfigParser()
    config.read(pargs.config)

    data = File.read_csv_to_list(config['MAILCONTENT']['maildata'])
    template = File.read_txt(config['MAILCONTENT']['mailtemplate'])

    send_to = dp.extract_fields(data, [int(i) for i in str(config['MAILCONTENT']['emailcolumns']).split(',')]) 
    column_data = dp.extract_fields(data, [int(i) for i in str(config['MAILCONTENT']['datacolumns']).split(',')])


    if pargs.sample:
        get_sample(send_to, template, column_data)
    elif pargs.nosend:
        for index, batch in enumerate(data):
            mail = Mail(send_to[index], "SAMPLE", template, column_data[index])
            print(str(mail))
    
    else:
        mail_list = []
        for index, batch in enumerate(data):
            mail = Mail(send_to[index], "SAMPLE", template, column_data[index])
            mail_list.append(mail)
            print(str(mail))

        print(config['ACCOUNT']['username'])
        print(config['MAIL']['mailserver'])
        print(int(config['MAIL']['mailport']))
    
        mail_blaster = EmailBlaster(config['ACCOUNT']['username'],
                                    config['MAIL']['mailserver'],
                                    int(config['MAIL']['mailport'])
                                    )
        mail_blaster.blast(mail_list)


if '__main__' == __name__:
    # No type check yet
    desp = 'THIS IS STILL UNDERDEVELOPMENT DO NOT USE\
            VERSION: 0.0.3\
            \
            To run: python3 blast.py -f '
            

    parser = argparse.ArgumentParser(description= desp)

    # Args 
    parser.add_argument('-s', '--sample', 
        help='Output sample content. [DOES NOT SEND]', action='store_true')
    parser.add_argument('-n', '--nosend',
        help='Output sample email. [DOES NOT SEND]', action='store_true')
    parser.add_argument('-f', '--config',
        help='Specify config file. [DOES NOT SEND]')


    pargs = parser.parse_args()

    
    main()