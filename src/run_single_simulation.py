#!/usr/bin/env python3

from time import sleep
from os import mkdir
import argparse

from helper import print_with_timestamp, get_iso_time, get_epoch

from download_logs import download_logs
from vmcontrol.sessionhandler import SessionHandler
from vmcontrol.vmmcontroller import VBoxController
from attacks.attack import AttackException

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

TOTAL_SIM_DURATION = 120 * 60
START_WAIT_DURATION = 60 * 60
WAIT_BETWEEN_STEPS = 5 * 60


def main():
    args = parse_args()
    run_simulation(args.sim_id)


def parse_args():
    parser = argparse.ArgumentParser(description="Run SOCBED simulation and download logs")
    parser.add_argument("sim_id", help="Identifier for this simulation run (aka directory name)")
    return parser.parse_args()


def run_simulation(sim_id):
    sim_start, sim_end, session_handler = start_session(sim_id)
    try:
        run_attacks(sim_start, sim_id)
        close_session(sim_start, sim_end, sim_id, session_handler)
    except (ValueError, AttackException, KeyboardInterrupt) as e:
        print("Something went wrong, shutting down session and exiting...")
        session_handler.close_session()
        exit(1)


def start_session(sim_id):
    sim_start = get_epoch()
    sim_end = get_epoch() + TOTAL_SIM_DURATION
    session_handler = SessionHandler(VBoxController())

    print_with_timestamp(f"Creating directory {sim_id}/ for log storage...")
    mkdir(sim_id)

    print_with_timestamp(f"Starting session {sim_id}...")
    session_handler.start_session()

    print_with_timestamp(f"Session is up. Waiting until {int(START_WAIT_DURATION / 60)} minutes have passed...")
    try:
        sleep(sim_start + START_WAIT_DURATION - get_epoch())
    except KeyboardInterrupt:
        print("Closing session and exiting...")
        session_handler.close_session()
        exit(1)

    return sim_start, sim_end, session_handler


def run_attacks(sim_start, sim_id):
    print_with_timestamp("Running multi-step attack (pausing ~1 minute before "
                         f"and ~{int((WAIT_BETWEEN_STEPS-60)/60)} minutes after each step)...")
    for counter, attack in enumerate(attacks, start=1):
        run_single_attack(attack, sim_start, sim_id, counter)


def run_single_attack(attack, sim_start, sim_id, counter):
    attack_start_time = get_epoch()
    attack_name = attack.__class__.__name__
    sleep(60)

    print_with_timestamp(f"Running {attack_name}...")
    attack.run()

    sleep(sim_start + START_WAIT_DURATION + counter * WAIT_BETWEEN_STEPS - get_epoch())
    attack_end_time = get_epoch()

    # Due to a bug with the SOCBED clients, timestamps for winlogbeat need to be set back by one hour
    print_with_timestamp(f"Downloading logs for {attack_name}...\n"
                         f"Start timestamp: {get_iso_time(attack_start_time-3600)}\n"
                         f"End timestamp: {get_iso_time(attack_end_time-3600)}")
    download_logs(start=get_iso_time(attack_start_time-3600),
                  end=get_iso_time(attack_end_time-3600),
                  suffix=attack_name,
                  save_dir=sim_id)


def close_session(sim_start, sim_end, sim_id, session_handler):
    print_with_timestamp(f"Waiting until {int(TOTAL_SIM_DURATION / 60)} minutes have passed...")
    sleep(sim_end - get_epoch())

    # Due to a bug with the SOCBED clients, timestamps for winlogbeat need to be set back by one hour
    print_with_timestamp("Downloading logs for entire simulation...\n"
                         f"Start timestamp: {get_iso_time(sim_start-3600)}\n"
                         f"End timestamp: {get_iso_time(sim_end-3600)}")
    download_logs(start=get_iso_time(sim_start-3600),
                  end=get_iso_time(sim_end-3600),
                  suffix="EntireSimulation",
                  save_dir=sim_id)

    print_with_timestamp("Closing session...")
    session_handler.close_session()

    print_with_timestamp("Done.")


if __name__ == "__main__":
    main()
