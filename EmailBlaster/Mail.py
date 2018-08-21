#! /usr/bin/env python3
###############################################################################
# Name: Mail.py                                                               #
# Description: Mail object                                                    #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
#                                                                             #
###############################################################################

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Mail:
    
    send_to = ''
    message = ''
    attachment = None 


    message_data = []
    message_template = ''


    def __init__(self, send_to: str, subject: str, message_template: str, 
        message_data: list):
        """
        Constructor to the Mail object
        @param send_to: who
        @param message_template: The template message that is not formatted
        @param message_data: The data that is to be sub in 
        @param attachment: The Attachment
        """

        self.send_to = send_to
        self.message = message_template.format(message_data)
        self.subject = subject


    def __str__(self):
        """
        A magic function to get string 
        """
        buffer = 'To:{}\n {}'.format(','.join(self.send_to), ''.join(self.message))
        return buffer

    
    def craft(self, username):
        msg_obj = MIMEMultipart()
        msg_obj['Subject'] = self.subject
        msg_obj['To'] = ', '.join(self.send_to)
        msg_obj['From'] = username

        msg_obj.attach(MIMEText(self.message,'html'))
        return msg_obj.as_string()

    def getaddr(self):
        return self.send_to.join(',') 