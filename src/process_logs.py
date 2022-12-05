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
             "EntireSimulation"]


def main():
    args = parse_args()
    process_logs(args.sim_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Process logs using chainsaw")
    parser.add_argument("sim_id", help="Identifier of a simulation run (aka directory)")
    return parser.parse_args()


def process_logs(sim_id):
    sim_id = sim_id.rstrip("/")

    for log_file in log_files:
        print_with_timestamp(f"Processing logs for {log_file}")

        jsonl_input = f"{sim_id}/{log_file}_winlogbeat.jsonl"
        output = f"{sim_id}/{log_file}_sigma.txt"

        command = chainsaw_command(jsonl_input, output)
        call(command)

        output = f"{sim_id}/{log_file}_sigma.json"
        command = chainsaw_command(jsonl_input, output)
        call(command)


def chainsaw_command(jsonl_input, output):
    command = ["./src/chainsaw",
               "hunt",
               f"{jsonl_input}",
               "--sigma",
               "sigma/rules/",
               "--mapping",
               "labeling_metadata/winlogbeat_sigma_mapping.yml",
               "--output",
               f"{output}",
               "--load-unknown"]
    if ".json" in output:
        command.append("--json")
    return command


if __name__ == "__main__":
    main()
