import argparse
import json
import pprint


def main():
    args = parse_args()
    rule_counts = {}
    with open(args.filename, 'r') as f:
        for line in f:
            event = json.loads(line)
            for rule in event['rule']:
                if true_positive(rule, event['event']):
                    rule_counts[rule] = rule_counts.get(rule, 0) + 1
    pprint.pprint(rule_counts)


def parse_args():
    parser = argparse.ArgumentParser(description='Count True Positives')
    parser.add_argument('filename', help='JSONL input file')
    return parser.parse_args()


def true_positive(rule, winlog):
    if (
            # c2_mimikatz
            (rule == 'Meterpreter or Cobalt Strike Getsystem Service Start') or
            # 2x misc_download_malware
            (rule == 'Windows PowerShell Web Request' and
             'meterpreter_bind_tcp.exe' in winlog['process']['command_line']) or
            # 1x misc_download_malware
            (rule == 'Non Interactive PowerShell' and
             'meterpreter_bind_tcp.exe' in winlog['process']['command_line']) or
            # 1x misc_set_autostart
            (rule == 'Direct Autorun Keys Modification' and
             'Meterpreter Bind TCP' in winlog['process']['command_line']) or
            # 1x misc_set_autostart
            (rule == 'Autorun Keys Modification' and
             winlog['registry']['value'] == 'Meterpreter Bind TCP')
    ):
        return True
    return False


if __name__ == '__main__':
    main()
