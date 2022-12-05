## Files in this directory

`winlogbeat_sigma_mapping.yml`:
- mapping to be used by chainsaw
- specifically for Sigma rules and `.jsonl` data
- includes a set of exceptions to prevent certain rules from triggering when their conditions are not met

`rule_dict.json`
- dictionary of rules and their conditions used by the Python labeling script to determine true/false positives
- only contains rules that were observed during testing
- content of a single entry:
  - link to rule in Sigma repo
  - information about what causes true positives
  - information about what causes false positives
  - list of conditions to be used by the labeling script (none if the rule only has false positives). A condition consists of
    - name of the relevant log field
    - expected content of that field
