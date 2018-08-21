#! /usr/bin/env python3
###############################################################################
# Name: EmailBlaster.py                                                       #
# Description: Blaster                                                        #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################


import smtplib
import getpass
import time

class EmailBlaster:

    username = ''
    mailserver = ''
    mailport = int()

    def __init__(self,username, mailserver, mailport ):

        self.username = username
        self.mailserver = mailserver
        self.mailport = mailport


    def blast(self, mail_list: list):
        with smtplib.SMTP(self.mailserver, self.mailport) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.set_debuglevel(1)
            print('LOGGING INTO EMAIL')
            smtp.login(self.username, getpass.unix_getpass())
            print('LOG IN SUCCESSFUL')
            # for email in mail_list:
            #     smtp.sendmail(self.username, email.getaddr(),
            #     email.craft)

            print('sleeping')
            time.sleep(5)
        print('DONE')