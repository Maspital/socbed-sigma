import argparse
import json
from pprint import pprint
import re

from helper import extend_filename


def main():
    args = parse_args()
    logfile, rules_dict = open_json_files(args.logfile, args.rules_dict)
    rule_counts = {}

    for sigma_alert in logfile:
        rule = sigma_alert["name"]
        if is_true_positive(sigma_alert, rule, rules_dict):
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
            label_alert(sigma_alert, True)
        else:
            label_alert(sigma_alert, False)
        rename_fields(sigma_alert)

    print("Rule hits (true positives):")
    pprint(rule_counts)

    save_result(data=logfile,
                new_filename=extend_filename(args.logfile, "LABELED"))


def parse_args():
    parser = argparse.ArgumentParser(description='Count True Positives')
    parser.add_argument("logfile", help='JSON log file')
    parser.add_argument("rules_dict", help="dictionary containing rules for labeling")
    return parser.parse_args()


def is_true_positive(sigma_alert, rule, rules_dict):
    label = False
    target_rule_content = {}

    # there are certainly more efficient ways to do this, but runtime is still fairly short, so ¯\_(ツ)_/¯
    for rule_name, content in rules_dict.items():
        if rule_name == rule:
            target_rule_content = content
            break

    try:
        for condition in target_rule_content["conditions"].values():
            if condition_is_met(sigma_alert, condition):
                label = True
                break
    except KeyError:
        return label

    return label


def condition_is_met(sigma_alert, condition):
    # NOTE: assumes key name itself NEVER contains a dot (.)
    relevant_dict_entry = condition[0].split(".")
    desired_content = convert_string_to_regex_pattern(condition[1])
    actual_content = sigma_alert

    # iterate into the dict structure
    for key in relevant_dict_entry:
        try:
            actual_content = actual_content.get(key)
        except AttributeError:
            return False

    return desired_content.match(actual_content)


def label_alert(sigma_alert, label):
    sigma_alert["metadata"] = {}
    sigma_alert["metadata"]["misuse"] = label


def rename_fields(sigma_alert):
    try:
        sigma_alert["rule"] = sigma_alert.pop("name")
    except KeyError:
        pass

    try:
        sigma_alert["event"] = sigma_alert["document"].pop("data")
    except KeyError:
        pass


def convert_string_to_regex_pattern(string):
    # escape all chars that matter for regex
    for char in ["\\", ".", "^", "$", "*", "+", "?", "(", ")", "[", "{", "|"]:
        string = string.replace(char, f"\\{char}")

    # convert keywords to appropriate regex expression
    string = string.replace("ANY_WORD_CHARS", r"\w+")

    return re.compile(string)


def open_json_files(logfile, rules_dict):
    with open(logfile) as json_file:
        json_data = json.load(json_file)

    with open(rules_dict) as json_file:
        json_rules = json.load(json_file)

    return json_data, json_rules


def save_result(data, new_filename):
    print(f"Saving labeled dataset to new file {new_filename}.")
    with open(new_filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
