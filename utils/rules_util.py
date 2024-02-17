import logging
import os
import json5
from models.data_model import ValidationRules
RULES = dict()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("rules_util")


def read_rules_json(rules_folder_path, rules_file):
    rules_file_path = os.path.join(rules_folder_path, rules_file)

    with open(rules_file_path, 'r') as file:
        data = json5.load(file)
    return data


def load_rules(rules_folder_path, rules_file):
    global RULES
    data = read_rules_json(rules_folder_path, rules_file)
    rules: ValidationRules = ValidationRules(**data['rules'])
    log.info(rules)
    return rules
