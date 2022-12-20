from src.utils.all_utils import read_yaml, get_template_from_txt
from src.utils.send_email import send_email
import argparse
import pandas as pd
import os
import PyPDF2
import re
import docx2txt


def get_data(config_path, f_name):
    config = read_yaml(config_path)
    binder_dir = config["artifacts"]['binder_dir']
    f_path = binder_dir + '/' + f_name
    if f_name.endswith('.pdf'):
        pdfFileObj = open(f_path, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # Iterate through each pdf page content texts
        for page in range(0, pdfReader.numPages):
            pageObj = pdfReader.getPage(page)
            doc_text = pageObj.extractText()
            # Choose the appropriate template based on the rules in the config file
            binder_rules = config["binder_rules"]
            template_name = get_template_from_txt(doc_text, binder_rules)
            return template_name
            break
    elif f_name.endswith('.docx'):
        doc_text = docx2txt.process(f_path)
        # Choose the appropriate template based on the rules in the config file
        binder_rules = config["binder_rules"]
        template_name = get_template_from_txt(doc_text, binder_rules)
        return template_name


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Process the binders')
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--file", "-f")
    parsed_args = args.parse_args()
    template_name = get_data(config_path=parsed_args.config, f_name=parsed_args.file)
    print("template name is --", template_name)
    
    sender =     ''
    destination = ['']
    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'
    content="""\
    Test message
    """
    subject="Thanks for emailing us"
    
    print(send_email(destination, sender, subject, msg="Hi"))

