import argparse
import pathlib

from helper import get_iso_time
from run_single_simulation import run_simulation
from process_logs import process_logs
from label_sigma import label_sigma

rules_dict_path = _repo_root_dir = pathlib.Path(__file__).resolve().parents[1].joinpath(
    "labeling_metadata/rule_dict.json")


def main():
    args = parse_args()

    if args.action == "generate":
        sim_id = get_iso_time(include_ms=False)
        run_simulation(sim_id)
        process_logs(sim_id)
    elif args.action == "label":
        if not args.path:
            print_error_msg()
        label_sigma(logfile_name=args.path, rules_dict=rules_dict_path)
    else:
        print_error_msg()


def parse_args():
    parser = argparse.ArgumentParser(description="Generate and evaluate log data from SOCBED")
    parser.add_argument("action", help="Action you want to take, either 'generate' or 'label'.\n"
                        "'label' action requires a path")
    parser.add_argument("--path", help="Path to *sigma.json dataset to label with the 'label' action")
    return parser.parse_args()


def print_error_msg():
    print("Unknown action or missing path. Supported commands:\n"
          "socbed_sigma generate: Generates a new dataset"
          "socbed_sigma label <sigma_file>: Label a given dataset")


if __name__ == '__main__':
    main()
