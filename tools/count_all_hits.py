import argparse
import json
from pprint import pprint


def main():
    args = parse_args()
    with open(args.logfile) as json_file:
        json_data = json.load(json_file)

    rule_counts = {}
    for sigma_alert in json_data:
        rule = sigma_alert["name"]
        rule_counts[rule] = rule_counts.get(rule, 0) + 1

    print("All hits:")
    pprint(rule_counts)


def parse_args():
    parser = argparse.ArgumentParser(description='Count all rule hits')
    parser.add_argument('logfile', help='JSON log file')
    return parser.parse_args()


if __name__ == '__main__':
    main()
