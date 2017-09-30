#!/usr/bin/python3
import smtplib, time
from time import gmtime, strftime
#####################################
#              File IO              #
#####################################
TEMPLATE_FILE = "EmailTemplate.txt" # File to read the template from

DATA_FILE = "data.tsv" # File to read the data to input from
DATA_SKIP_FIRST_ROW = True # Skip the first row if the first row is the column names
DATA_SEPERATOR = u"\t" # The seperator used to differentiate columns

######################################
#            EMAIL SERVER            #
######################################
HOST = "smtp.example.com" # Host of the email server to conenct to
PORT = 587 # TLS Port number of the email server to connect to
USERNAME = "email@example.com" # Username to authenticate and send mail as
PASSWORD = "password" # Password to authenticate the user

FROM_ADDR = "from@example.com" # Displayed address to send the email from
TO_ADDR_ID = [2]
CC_ADDR_ID = [4, 6, 8] # Address IDs to read from in the data file. Values count from 0.
BCC_ADDR_ID = []
SUBJECT = "A very important message" # Subject of the email

def main():
    print("Connecting to SMTP server...")
    smtp = smtplib.SMTP(HOST, PORT)
    smtp.ehlo()
    smtp.starttls() # Start the TLS handshake with the mailserver.
    smtp.ehlo()
    print("Logging into the SMTP server...")
    smtp.login(USERNAME, PASSWORD)
    # Uncomment the following line to view debigging information
	# smtp.set_debuglevel(1)

    with open(TEMPLATE_FILE) as template_file:
        print("Reading Email Template...")
        template_text = template_file.read()
        with open(DATA_FILE) as data_file:
            print("Reading Data Template...")
            header = True
            for line in data_file:
                # Skip first line
                if header and DATA_SKIP_FIRST_ROW:
                    header = False
                    continue

                # Split the data file
                data_line = line.strip().split(DATA_SEPERATOR)

                # Get the TO, CC and BCC address from the split line
                to_addr = [data_line[i] for i in TO_ADDR_ID]
                cc_addr = [data_line[i] for i in CC_ADDR_ID]

                # Format the message
                message = template_text.format(*data_line)
                full_message = "From: {}\r\n".format(FROM_ADDR) \
                               + "To: {}\r\n".format(", ".join(set(to_addr))) \
                               + "CC: {}\r\n".format(", ".join(set(cc_addr))) \
                               + "Subject: {}\r\n".format(SUBJECT)+ "\r\n" \
                               + message

                to_addrs = to_addr + cc_addr

                print("Sending mail to:", ", ".join(set(to_addrs)))
                # print(full_message)
                smtp.sendmail(FROM_ADDR, to_addrs, full_message)

                print("Waiting 2 seconds for anti-spam prevention...")
                time.sleep(2)

            data_file.close()
        template_file.close()
    print("Mail sending completed.")
    smtp.quit()

if __name__ == "__main__":
    main()
