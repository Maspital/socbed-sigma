import argparse
import json
from pprint import pprint
import re

from helper import extend_filename


def main():
    args = parse_args()
    label_sigma(args.logfile, args.rules_dict)


def parse_args():
    parser = argparse.ArgumentParser(description='Count and label true positives')
    parser.add_argument("logfile", help='Single JSON log file containing Sigma alerts to label')
    parser.add_argument("rules_dict", help="dictionary containing rules for labeling")
    return parser.parse_args()


def label_sigma(sim_id, rules_dict):
    logfile, rules_dict = open_json_files(sim_id, rules_dict)

    label_alerts(logfile, rules_dict)
    save_result(data=logfile,
                new_filename=extend_filename(sim_id, "LABELED", ".jsonl"))


def label_alerts(logfile, rules_dict):
    tp_counts = {}
    fp_counts = {}

    for sigma_alert in logfile:
        rule = sigma_alert["name"]
        if is_true_positive(sigma_alert, rule, rules_dict):
            tp_counts[rule] = tp_counts.get(rule, 0) + 1
            apply_label(sigma_alert, True)
        else:
            fp_counts[rule] = fp_counts.get(rule, 0) + 1
            apply_label(sigma_alert, False)
        rename_fields(sigma_alert)

    print_results(tp_counts, fp_counts)


def is_true_positive(sigma_alert, rule, rules_dict):
    target_rule_content = {}

    # there are certainly more efficient ways to do this, but runtime is still fairly short, so ¯\_(ツ)_/¯
    for rule_name, content in rules_dict.items():
        if rule_name == rule:
            target_rule_content = content
            break

    if not target_rule_content:
        print(f"\033[93m[WARNING]\033[0m Unknown alert: {rule}")
        return False

    conditions = target_rule_content["conditions"].values()
    label = len(conditions) > 0 and any(condition_is_met(sigma_alert, con) for con in conditions)

    return label


def condition_is_met(sigma_alert, condition):
    # NOTE: assumes key name itself NEVER contains a dot (.)
    relevant_dict_entry = condition[0].split(".")
    desired_content = re.compile(condition[1])
    actual_content = sigma_alert

    # iterate into the dict structure
    for key in relevant_dict_entry:
        try:
            actual_content = actual_content.get(key)
            # Some entries may come as lists. If that's the case, we only want the first entry to proceed
            if isinstance(actual_content, list):
                actual_content = actual_content[0]
        except AttributeError:
            return False

    return desired_content.match(actual_content)


def apply_label(sigma_alert, label):
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


def print_results(tp_counts, fp_counts):
    print("Rule hits (true positives):")
    pprint(tp_counts)
    print("Rule hits (false positives):")
    pprint(fp_counts)


def save_result(data, new_filename):
    print(f"Saving labeled dataset to new file {new_filename}.")
    with open(new_filename, "w") as file:
        for entry in data:
            json.dump(entry, file)
            file.write("\n")


if __name__ == '__main__':
    main()
