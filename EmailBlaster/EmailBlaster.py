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
    mailsender_address = ''
    mailsender_name = ''
    mailserver = ''
    mailport = int()

    def __init__(self, username, mailsender_address, mailsender_name, mailserver, mailport):
        """
        Constructor
        
        @param username: the username of the email
        @param mailserver: url to the mailserver
        @param mailport: the port 
        """
        self.username = username
        self.mailsender_address = mailsender_address
        self.mailsender_name = mailsender_name
        self.mailserver = mailserver
        self.mailport = mailport


    def blast(self, mail_list: list):
        """
        Send the batch

        @param mail_list: The list of mail object
        """
        with smtplib.SMTP(self.mailserver, self.mailport) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.set_debuglevel(1)
            print('LOGGING INTO EMAIL')
            smtp.login(self.username, getpass.getpass())
            print('LOG IN SUCCESSFUL')
            # Prevent sending in development
            for email in mail_list:
                smtp.sendmail(self.mailsender_address, email.getaddr(),
                              email.craft(self.mailsender_address, self.mailsender_name))
                #email.craft(self.username)
            print('sleeping')
            time.sleep(5)
        print('DONE')