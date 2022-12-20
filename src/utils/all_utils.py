import yaml
import os
import json
import re


def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content


def get_template_from_txt(doc_text: str, binder_rules: dict) -> str:
    for binder_name, rules in binder_rules.items():
#         print([str_rule for str_rule in rules['policy_names'].split(',')])
        match_policy_names = [True if re.search(str_rule, doc_text) else False for str_rule in
                              rules['policy_names'].split(',')]
#         print(match_policy_names)
        if any(match_policy_names):
            match_address = [True if re.search(str_rule, doc_text) else False for str_rule in
                             rules['location'].split(',')]
            return rules['name']
