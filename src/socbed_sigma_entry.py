import argparse
import pathlib
from sys import exit

from helper import get_iso_time
from run_single_simulation import run_simulation
from process_logs import process_logs
from label_sigma import label_sigma

repo_root_dir = pathlib.Path(__file__).resolve().parents[1]
rules_dict_path = repo_root_dir.joinpath("labeling_metadata/rule_dict.json")


def main():
    args = parse_args()
    if sum(bool(x) for x in [args.generate, args.process, args.label, args.full]) != 1:
        print_error_msg_and_exit(error="Please select exactly one action", err_code=1)

    elif args.generate:
        generate()
    elif args.process and args.path:
        process(args.path)
    elif args.label and args.path:
        label(args.path)
    elif args.full:
        sim_id = generate()
        process(sim_id)
        label(sim_id + "/Entire_Simulation_sigma.json")

    else:
        print_error_msg_and_exit(error="Unknown action or missing path", err_code=1)


def generate():
    sim_id = get_iso_time(include_ms=False, remove_colons=True)
    run_simulation(sim_id=sim_id)
    return sim_id


def process(sim_id):
    process_logs(sim_id=sim_id)


def label(sim_id):
    label_sigma(sim_id=sim_id, rules_dict=rules_dict_path)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate, process and label a log dataset using SOCBED and Sigma.\n"
                                                 "Only one action can be selected at once.")
    parser.add_argument("--generate", action="store_true",
                        help="Run a SOCBED simulation to generate log datasets.")
    parser.add_argument("--process", action="store_true",
                        help="Process a given log dataset using chainsaw, producing Sigma alerts. "
                             "Requires path to dataset directory.")
    parser.add_argument("--label", action="store_true",
                        help="Label a given set of Sigma alerts. Requires path to single .json file.")
    parser.add_argument("--full", action="store_true",
                        help="Generate, process and label a dataset (aka do everything).")
    parser.add_argument('path', type=str, nargs='?',
                        help="Path to *sigma.json dataset directory or file, "
                             "required when using '--process' or '--label'.")
    return parser.parse_args()


def print_error_msg_and_exit(error, err_code):
    print(f"{error}.\n"
          "Run 'socbed_sigma --help' for more information.")
    exit(err_code)


if __name__ == '__main__':
    main()
