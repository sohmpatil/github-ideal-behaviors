import logging
import os
import json5
from models.rules_model import ValidationRules
RULES = dict()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("rules_util")


def read_rules_json(rules_folder_path, rules_file):
    """
    Reads validation rules from a JSON file.

    This function reads a JSON file containing validation rules and returns a dictionary.

    Args:
        rules_folder_path (str): The path to the folder containing the rules file.
        rules_file (str): The name of the JSON file containing the rules.

    Returns:
        data: An dictionary containing the loaded validation rules.
    """
    rules_file_path = os.path.join(rules_folder_path, rules_file)

    with open(rules_file_path, 'r') as file:
        data = json5.load(file)
    return data


def load_rules(rules_folder_path, rules_file):
    """
    Loads validation rules from a JSON file.

    This function reads a JSON file containing validation rules and returns a ValidationRules object.

    Args:
        rules_folder_path (str): The path to the folder containing the rules file.
        rules_file (str): The name of the JSON file containing the rules.

    Returns:
        ValidationRules: An object containing the loaded validation rules.
    """
    global RULES
    data = read_rules_json(rules_folder_path, rules_file)
    rules: ValidationRules = ValidationRules(**data['rules'])
    log.info(rules)
    return rules
