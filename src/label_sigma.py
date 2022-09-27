import argparse
import json
from pprint import pprint

from helper import extend_filename


def main():
    args = parse_args()
    print(args.logfile)
    with open(args.logfile) as json_file:
        json_data = json.load(json_file)

    rule_counts = {}
    for sigma_alert in json_data:
        rule = sigma_alert["name"]
        if is_true_positive(sigma_alert, rule):
            rule_counts[rule] = rule_counts.get(rule, 0) + 1
            label_alert(sigma_alert, True)
        else:
            label_alert(sigma_alert, False)
        rename_fields(sigma_alert)

    print("Rule hits (true positives):")
    pprint(rule_counts)

    new_filename = extend_filename(args.logfile, "LABELED")
    print(f"Saving labeled dataset to new file {new_filename}.")
    with open(new_filename, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description='Count True Positives')
    parser.add_argument('logfile', help='JSON log file')
    return parser.parse_args()


def is_true_positive(sigma_alert, rule):
    command_line = get_command_line(sigma_alert)
    registry_value = get_registry_value(sigma_alert)
    if (
            # c2_mimikatz
            (rule == 'Meterpreter or Cobalt Strike Getsystem Service Start') or
            # 2x misc_download_malware
            (rule == 'Windows PowerShell Web Request' and
             'meterpreter_bind_tcp.exe' in command_line) or
            # 1x misc_download_malware
            (rule == 'Non Interactive PowerShell' and
             'meterpreter_bind_tcp.exe' in command_line) or
            # 1x misc_set_autostart
            (rule == 'Direct Autorun Keys Modification' and
             'Meterpreter Bind TCP' in command_line) or
            # 1x misc_set_autostart
            (rule == 'Autorun Keys Modification' and
             registry_value == 'Meterpreter Bind TCP')
    ):
        return True
    return False


def get_command_line(sigma_alert):
    if (
            "document" in sigma_alert and
            "data" in sigma_alert["document"] and
            "process" in sigma_alert["document"]["data"] and
            "command_line" in sigma_alert["document"]["data"]["process"]):
        return sigma_alert["document"]["data"]["process"]["command_line"]
    return None


def get_registry_value(sigma_alert):
    if (
            "document" in sigma_alert and
            "data" in sigma_alert["document"] and
            "registry" in sigma_alert["document"]["data"] and
            "value" in sigma_alert["document"]["data"]["registry"]):
        return sigma_alert["document"]["data"]["registry"]["value"]
    return None


def label_alert(sigma_alert, label):
    sigma_alert["metadata"] = {}
    sigma_alert["metadata"]["misuse"] = label


def rename_fields(sigma_alert):
    sigma_alert["rule"] = sigma_alert.pop("name")
    sigma_alert["event"] = sigma_alert["document"].pop("data")


if __name__ == '__main__':
    main()
