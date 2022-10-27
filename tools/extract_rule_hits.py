import argparse
import json
from os.path import dirname
from os import mkdir

rule_json = {"Cleartext Protocol Usage": 11,
             "Conhost Parent Process Executions": 3,
             "Creation of an Executable by an Executable": 57,
             "Direct Autorun Keys Modification": 1,
             "Encoded PowerShell Command Line Usage of ConvertTo-SecureString": 3,
             "Meterpreter or Cobalt Strike Getsystem Service Installation": 1,
             "Meterpreter or Cobalt Strike Getsystem Service Start": 1,
             "NTLMv1 Logon Between Client and Server": 1,
             "Non Interactive PowerShell": 16,
             "PowerShell DownloadFile": 3,
             "PowerShell Web Download": 3,
             "Process Start From Suspicious Folder": 1,
             "Rare Service Installations": 1,
             "Redirect Output in CommandLine": 1,
             "Reg Add RUN Key": 2,
             "Rename Common File to DLL File": 841,
             "Scheduled Task Creation": 1,
             "Startup Folder File Write": 12,
             "Suspicious Network Command": 18,
             "Verclsid.exe Runs COM Object": 5,
             "WMI Event Subscription": 18,
             "Windows Suspicious Use Of Web Request in CommandLine": 3}


def main():
    args = parse_args()
    mkdir(f"{dirname(args.logfile)}/{args.target_dir}")

    with open(args.logfile) as sigma_file:
        sigma_hits = json.load(sigma_file)

    filtered_json_by_user = filter_by_user("CLIENT1", sigma_hits)

    for rule_name in rule_json:
        filtered_json_by_rule = filter_by_rule(rule_name, filtered_json_by_user)

        clean_rule_name = get_clean_name(rule_name)
        full_filename = f"{dirname(args.logfile)}/{args.target_dir}/{clean_rule_name}.json"
        save_result(filtered_json_by_rule, full_filename)


def parse_args():
    parser = argparse.ArgumentParser(description='Extract hits for each separate alert')
    parser.add_argument('logfile', help='JSON log file')
    parser.add_argument('target_dir', help='new dir inside target folder to store results')
    return parser.parse_args()


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
    print(f"Saving labeled dataset to new file {filename}.")
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(json_result, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
