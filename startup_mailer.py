__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

import subprocess
import smtplib
import socket
import os

from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = '<insert your email address here>' # Email to send to.
gmail_user = '<insert your email address here>' # Email to send from. (MUST BE GMAIL)
gmail_password = '<insert your password>' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.

split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
# Get the current CPU speed
f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
cpu = f.read()
mail_body = "CPU speed: " + cpu + "IP address: %s" % ipaddr
msg = MIMEText(mail_body)
msg['Subject'] = "RasPI @ "+ipaddr+" started up on %s" % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
