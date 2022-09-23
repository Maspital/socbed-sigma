#!/usr/bin/env python3

from time import sleep
from os import mkdir
import argparse

from helper import print_with_timestamp, get_iso_time, get_epoch

from download_logs import download_logs
from vmcontrol.sessionhandler import SessionHandler
from vmcontrol.vmmcontroller import VBoxController

from attacks.attack_sqlmap import SQLMapAttack
from attacks.attack_email_exe import EmailEXEAttack
from attacks.attack_take_screenshot import TakeScreenshotAttack
from attacks.attack_c2_exfiltration import C2ExfiltrationAttack
from attacks.attack_mimikatz import MimikatzAttack
from attacks.attack_download_malware import DownloadMalwareAttack
from attacks.attack_set_autostart import SetAutostartAttack
from attacks.attack_execute_malware import ExecuteMalwareAttack

attacks = [SQLMapAttack(),
           EmailEXEAttack(),
           TakeScreenshotAttack(),
           C2ExfiltrationAttack(),
           MimikatzAttack(),
           DownloadMalwareAttack(),
           SetAutostartAttack(),
           ExecuteMalwareAttack()]


def main():
    args = parse_args()
    run_simulation(args.sim_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Run SOCBED simulation and download logs")
    parser.add_argument("sim_id", help="Identifier for this simulation run (aka directory name)")
    return parser.parse_args()


def run_simulation(sim_name):
    initial_wait = 10 * 60
    sim_start = get_epoch()
    sim_end = get_epoch() + 60 * 60
    sh = SessionHandler(VBoxController())

    print_with_timestamp(f"Creating directory {sim_name}/ for log storage...")
    mkdir(sim_name)

    print_with_timestamp(f"Starting session {sim_name}...")
    sh.start_session()

    print_with_timestamp("Session is up. Waiting until 10 minutes have passed...")
    sleep(sim_start + initial_wait - get_epoch())

    print_with_timestamp("Running multi-step attack (pausing ~2 minutes before and after each step)...")
    for counter, attack in enumerate(attacks, start=1):
        attack_start_time = get_iso_time()
        attack_name = attack.__class__.__name__
        sleep(2 * 60)

        print_with_timestamp(f"Running {attack_name}...")
        attack.run()

        sleep(sim_start + initial_wait + counter * 4 * 60 - get_epoch())
        attack_end_time = get_iso_time()

        print_with_timestamp(f"Downloading logs for {attack_name}...")
        download_logs(attack_start_time,
                      attack_end_time,
                      attack_name,
                      sim_name)

    print_with_timestamp("Waiting until 60 minutes have passed...")
    sleep(sim_end - get_epoch())
    print_with_timestamp("Downloading logs for entire simulation...")
    download_logs(get_iso_time(sim_start),
                  get_iso_time(sim_end),
                  "EntireSimulation",
                  sim_name)

    print_with_timestamp("Closing session...")
    sh.close_session()

    print_with_timestamp("Done.")


if __name__ == "__main__":
    main()
