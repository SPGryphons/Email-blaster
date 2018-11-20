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
from re import compile

class Mail:
    
    send_to = []
    cc_to = []
    message = ''
    attachment = None 


    message_data = []
    message_template = ''


    def __init__(self, send_to: list, subject: str, message_template: str,
        message_data: list, attachment=None):
        """
        Constructor to the Mail object
        @param send_to: who
        @param message_template: The template message that is not formatted
        @param message_data: The data that is to be sub in 
        @param attachment: The Attachment, in a 2D array

        returns mail
        """
        reg_data = compile(r'{(\d+)}') # Capture number inside curly brace placeholders
        message_template = reg_data.sub(r'{data[\1]}', message_template) # replace curly brace placeholders

        self.send_to = send_to
        self.message = message_template.format(data = message_data)
        self.subject = subject
        self.attachment = attachment


    def __str__(self):
        """
        A magic function to get string 
        """
        buffer = 'To: {}\nCC: {}\nSubject: {}\n{}\n{}' \
            .format(', '.join(self.send_to),
                ', '.join(self.cc_to),
                ''.join(self.subject),
                ''.join(self.message),
                '=' * 50
            )
            
        return buffer

    
    def craft(self, username, sendername):
        """
        Get the Mail object mail ready
        """
        msg_obj = MIMEMultipart()
        msg_obj['Subject'] = self.subject
        msg_obj['To'] = ', '.join(self.send_to)
        msg_obj['From'] = '\"{}\" <{}>'.format(sendername, username)
        if self.cc_to:
            msg_obj['CC'] = ', '.join(self.cc_to)

        msg_obj.attach(MIMEText(self.message, 'html'))

        # Added attachment support
        if self.attachment is not None:
            print(self.attachment)
            for attachment in self.attachment.keys():
                print(attachment)
                att_obj = MIMEBase('application', 'octet-stream')
                att_obj.set_payload(self.attachment[attachment])
                encoders.encode_base64(att_obj)
                att_obj.add_header('Content-Disposition', 'attachment', filename=attachment)
                msg_obj.attach(att_obj)
                
        return msg_obj.as_string()


    def set_cc(self, cc_to):
        self.cc_to = cc_to


    def getaddr(self):
        return self.send_to + self.cc_to