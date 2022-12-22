import sys
import os
import re
import smtplib             # use this for standard SMTP protocol   (port 25, no encryption)
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import listdir
from os.path import isfile, join
import PyPDF2
import re
import docx2txt
from src.utils.all_utils import read_yaml, get_template_from_txt

SMTPserver = 'tmu.mail.allianz'

def send_email(sender, destination, email_details_html):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart()
    msg['Subject'] = "Your Mailbox report is here!"
    msg['From'] = sender
    msg['To'] = destination

    # Create the body of the message (a plain-text and an HTML version).
    text = "Please see html file attached."
    dir_details = """
                <td>Alfreds Futterkiste</td>
                <td>Maria Anders</td>
                <td>Germany</td>
                <td>Germany</td>
                """
    
    html = """\
    <html>
      <head></head>
      <style>
            table, th, td {
              border:1px solid black;
            }
      </style>
      <body>
        <table style="width:100%">
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Sender Email</th>
                <th>Attachment File name</th>
                <th>Template Name</th>
              </tr>"""+email_details_html+"""
          </table>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(SMTPserver)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, destination, msg.as_string())
    s.quit()

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def get_data(config_path, f_path, f_name):
    config = read_yaml(config_path)
#     binder_dir = config["artifacts"]['binder_dir']
    f_path = f_path + '/' + f_name
    if f_name.endswith('.pdf'):
        pdfFileObj = open(f_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # Iterate through each pdf page content texts
        doc_text = ""
        for page in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            doc_text += pageObj.extractText()
            # Choose the appropriate template based on the rules in the config file
    
        binder_rules = config["binder_rules"]
        template_name = get_template_from_txt(doc_text, binder_rules)
        return template_name
    elif f_name.endswith('.docx'):
        doc_text = docx2txt.process(f_path)
        # Choose the appropriate template based on the rules in the config file
        binder_rules = config["binder_rules"]
        template_name = get_template_from_txt(doc_text, binder_rules)
        return template_name
    
if __name__ == '__main__':
    text_subtype = 'html'
    sender_email =     'sarath.cp1@allianz.com'
    destination_emails = 'sarath.cp1@allianz.com'
    
    email_details_html = ""

    path = "./binder_files/downloads"
    date_folders = get_immediate_subdirectories(path)
    data_list = []
    
    emails_in_day_list = []
    for date in date_folders:
        emails_list = get_immediate_subdirectories(path+'/'+date)
        for email in emails_list:
            try:
                time_and_sender = email.split('-')
                attached_files = ""
                for file in get_files(path+'/'+date+'/'+email):
                    attached_files = file
                sender = time_and_sender[1]
                time = time_and_sender[0]
            except:
                sender = ""
                time = ""
                attached_files = ""
            f_path = path+'/'+date+'/'+email
            template_name = get_data("config/templates_config.yaml", f_path, attached_files)
            if time and sender:
                emails_in_day_list.append([date,time,sender,attached_files, template_name])
    for email_data in emails_in_day_list:
        email_details_html += '<tr>'
        for data in email_data:
            email_details_html += '<td>{}</td>'.format(data)
        email_details_html += '</tr>'
    send_email(sender_email, destination_emails, email_details_html)