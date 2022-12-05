import argparse
import json
from os.path import dirname
from os import mkdir


def main():
    args = parse_args()
    mkdir(f"{dirname(args.logfile)}/{args.target_dir}")

    with open(args.logfile) as sigma_file:
        sigma_hits = json.load(sigma_file)

    rule_list = count_rule_types(sigma_hits)
    filtered_json_by_user = filter_by_user("CLIENT1", sigma_hits)

    for rule_name in rule_list:
        filtered_json_by_rule = filter_by_rule(rule_name, filtered_json_by_user)

        clean_rule_name = get_clean_name(rule_name)
        full_filename = f"{dirname(args.logfile)}/{args.target_dir}/{clean_rule_name}.json"
        save_result(filtered_json_by_rule, full_filename)


def parse_args():
    parser = argparse.ArgumentParser(description='Extract hits for each separate alert (only for CLIENT 1)')
    parser.add_argument('logfile', help='JSON log file')
    parser.add_argument('target_dir', help='new dir inside target folder to store results')
    return parser.parse_args()


def count_rule_types(json_file):
    rule_list = []

    for sigma_alert in json_file:
        try:
            rule = sigma_alert["name"]
            if rule not in rule_list:
                rule_list.append(rule)
        except KeyError:
            pass
    return rule_list


def filter_by_user(user_name, json_file):
    output = []

    for sigma_alert in json_file:
        try:
            name = sigma_alert["document"]["data"]["agent"]["name"]
            if name == user_name:
                output.append(sigma_alert)
        except KeyError:
            pass
    return output


def filter_by_rule(rule_name, json_file):
    output = []
    counter = 0

    for sigma_alert in json_file:
        try:
            rule = sigma_alert["name"]
            if rule == rule_name:
                output.append(sigma_alert)
                counter += 1
        except KeyError:
            pass

    output.append({"total_hits": counter})
    return output


def get_clean_name(name):
    name = name.replace(" ", "_")
    name = name.replace(".", "_")
    name = name.lower()
    return name


def save_result(json_result, filename):
    print(f"Saving extracted alerts to new file {filename}.")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(json_result, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
