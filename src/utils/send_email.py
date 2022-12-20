import sys
import os
import re
from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.mime.text import MIMEText
SMTPserver = 'tmu.mail.allianz'


def send_email(destination, sender, subject, msg):
    try:
        msg = MIMEText(content, text_subtype)
        msg['To'] = ','.join(destination)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all
        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
        return("Successfully sent email")
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message
        return("Email send failed")
    
    
