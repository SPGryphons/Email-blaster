#! /usr/bin/python3
# Coded by kai mun
# import all the nessesary library
import smtplib
import os
import argparse
import sys
import configparser
import pandas as pd
import csv
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Generating the config file that has the extension of ini
def config_gen():
    config = configparser.ConfigParser()
    # Creating the DEFAULT SECTION CONFIG
    config['DEFAULT'] = {'username': 'Put the username here',
                          'password': 'put the password here',}
    with open('account.ini', 'w+') as configfile:
        config.write(configfile)


# reading from file
def read_acct(path):
    # reading the file from the account file 
    # path = 'account.txt'
    try:
        # This will store the account and callable by name
        config = configparser.RawConfigParser()
        config.read('account.ini')

        account = {'username': config['DEFAULT']['username'],
                   'password': config['DEFAULT']['password']
                   }
        #Does no check for empty password or username
        return account

    except(FileNotFoundError):
        print('The account file is not found...')


# Reading in the send list
def read_address(path):
    # path = 'contact.txt'
    try:
        with open(path, 'r') as file:
            contact_df = pd.read_table(file, sep='\t')
            #print(contact_df)
            return contact_df
    except FileNotFoundError:
        print('No contact file')


# reading data file, only for txt, if mod is need use %s% as placeholder
def read_content(path):
    # path = './content.txt'
    try:
        with open(path, 'r') as file:
            content = file.readlines()
            # Joining the elements
            content = ''.join(content)
    except FileNotFoundError:
        print('There is no content...')

    return content


# Putting here first, no idea if it will work
def mod_content(content, change_list):
    # Going to add handle for error in the future
    for i in range(len(change_list)):
        change_list[i] = str(change_list[i])
    print(change_list)


    content = content.format(*change_list)
    return content

# Reading in file, sending using MIMEMultipart
def read_file(mail_obj, attachment):
    attachment = attachment.split(',')
    try:
        for file in attachment:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', 'octet-stream')
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                mail_obj.attach(msg)
    except:
        print('Error reading file, ERROR: ', sys.exc_info()[0])


def main():
    
    # Handling the current config generation since the password is not in,
    # We stop the run and config
    if args.generate_config:
        print('Generating the configuration off template')
        config_gen()
        print('Done generating')
        exit(0)

    SUBJECT = args.subject
    account = read_acct(args.particular)
    sendtable = read_address(args.to)
    if args.content is not None:
        content = read_content(args.content)
    email_col = args.email_columns
    content_col = args.content_columns
    emails = sendtable.iloc[:, email_col]
    content_mod = sendtable.iloc[:, content_col]
    if args.webformat is not None:
        html = read_content(args.webformat)

    if args.verbose:
        print('content file: {}'.format(args.content))
        print('Subject: {}'.format(SUBJECT))
        print('Email columns: '.format(email_col))
        print('Credential: '.format(account))
        print(sendtable.index)
        if args.content is not None:
            print(content)
        else:
            print(html)
        print('Emailing: ', list(emails.iloc[0]))
        print('Adding in: ', list(content_mod.iloc[1]))
    if args.nosend:
        print('ending without sending...')
        exit(0)

    for i in sendtable.index:
        sendlist = list(emails.iloc[i])
        mod_content_list = list(content_mod.loc[i])
        content_mod_check = args.mode
        msg_obj = MIMEMultipart()
        msg_obj['Subject'] = SUBJECT
        msg_obj['To'] = ', '.join(sendlist)
        msg_obj['From'] = account['username']

        # Preamble 
        msg_obj.preamble = 'email is not mime aware'

        if args.content is not None:
            if content_col is not None and content_mod_check is 'c':
                content = mod_content(content, mod_content_list)
            msg_obj.attach(MIMEText(content, 'plain'))

        if args.webformat is not None and args.webformat.endswith('html'):
            if content_col is not None and content_mod_check is 'h':
                html_buf = mod_content(html, mod_content_list)
            msg_obj.attach(MIMEText(html_buf,'html'))

        if args.attachment is not None:
            attachment = args.attachment
            print(attachment)
            read_file(msg_obj, attachment)

        composed = msg_obj.as_string()

        # sending mail
        try:
            with smtplib.SMTP('smtp.zoho.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.set_debuglevel(1)
                print('LOGGING INTO EMAIL')
                smtp.login(account['username'], account['password'])
                print('LOG IN SUCCESSFUL')
                smtp.sendmail(account['username'], sendlist, composed)
            print('DONE')
            print('sleeping')
            time.sleep(5)
        except:
            print('Unexpected ERROR', sys.exc_info()[0])
            raise
if '__main__' == __name__:
    # No type check yet
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--attachment', help='path to the attachment(s)')
    parser.add_argument('-c', '--content', help='path to the content file')
    parser.add_argument('-t', '--to', help='The file that holds the address')
    parser.add_argument('-p', '--particular', help='the file that has your credentials')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    parser.add_argument('-g', '--generate-config', action='store_true', help='To generate the config file')
    parser.add_argument('-n', '--nosend', action='store_true', help='dont send email')
    parser.add_argument('-e', '--email_columns', type=int, metavar='N', nargs='+', help='column(s) that contains email that you want to sent to')
    parser.add_argument('-s', '--subject', default='TEST', nargs='+' ,help='email subject')
    parser.add_argument('-m', '--content_columns', nargs='+', type=int, metavar='c', help='content column(s)' )
    parser.add_argument('-w', '--webformat', help='html file')
    parser.add_argument('-z', '--mode', help='Choosing the type of file to send (c) for normal, (h) for html') # temporary
    args = parser.parse_args()
    main()
