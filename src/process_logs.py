#!/usr/bin/env python3

import argparse
from subprocess import call

from helper import print_with_timestamp

log_files = ["SQLMapAttack",
             "EmailEXEAttack",
             "TakeScreenshotAttack",
             "C2ExfiltrationAttack",
             "MimikatzAttack",
             "DownloadMalwareAttack",
             "SetAutostartAttack",
             "ExecuteMalwareAttack",
             "complete"]


def main():
    args = parse_args()
    process_logs(args.sim_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Process logs using chainsaw")
    parser.add_argument("sim_id", help="Identifier of a simulation run (aka directory)")
    return parser.parse_args()


def get_command(jsonl_input, output):
    command = ["./src/chainsaw",
               "hunt",
               f"{jsonl_input}",
               "--sigma",
               "sigma/rules/",
               "--mapping",
               "mappings/winlogbeat_sigma_mapping.yml",
               "--output",
               f"{output}",
               "--load-unknown"]
    if ".json" in output:
        command.append("--json")
    return command


def process_logs(sim_id):
    for log_file in log_files:
        print_with_timestamp(f"Processing logs for {log_file}")

        jsonl_input = f"{sim_id}/{log_file}_winlogbeat.jsonl"
        output = f"{sim_id}/{log_file}_sigma.txt"

        command = get_command(jsonl_input, output)
        call(command)

        output = f"{sim_id}/{log_file}_sigma.json"
        command = get_command(jsonl_input, output)
        call(command)


if __name__ == "__main__":
    main()
