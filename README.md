### Prerequisites
- Configure and build SOCBED as described in the base [SOCBED repository](https://github.com/fkie-cad/socbed)

Further instructions assume that your current directory is the base directory of this repository.
- Install additional dependencies in your SOCBED virtual environment (that you created while installing SOCBED)
    ```shell
    source ~/.virtualenvs/socbed/bin/activate
    pip install elasticsearch elasticsearch-dsl
    ```
- Download and extract Chainsaw v2.1.0 (find more info about Chainsaw [here](https://github.com/WithSecureLabs/chainsaw))
    ```shell
  wget -O chainsaw.tar.gz https://github.com/WithSecureLabs/chainsaw/releases/download/v2.1.0/chainsaw_x86_64-unknown-linux-gnu.tar.gz
  tar -xf chainsaw.tar.gz
  mv chainsaw/chainsaw src/
  rm -rf chainsaw* # we only need the binary
    ```


### Generating log files and alerts
This process will take approximately 65 minutes.
```shell
source ~/.virtualenvs/socbed/bin/activate
./evaluate
```
Afterwards, you will find another directory named after the starting time of your simulation (note that all times are UTC).
Therein, you will find three types of files, once for each attack and once for the entire simulation:
- `*_winlogbeat.jsonl`, containing all logs produced by SOCBED clients during a given time
- `*_sigma.txt`, containing generated SIGMA alerts from the log-file of the same name in human-readable form
- `*_sigma.json`, containing generated SIGMA alerts from the log-file of the same name in json format for easier parsing


### Evaluate log files
TODO
- Determine if all expected alerts have been found
- Ensure each expected alert actually originated from the expected source (an attack)
  - Could be done by checking certain fields
    - timestamp
    - CommandLine
    - Parent or similar (many attacks originate from ssh user)
    - Details
    - message (contains a BUNCH of info, probably the best solution)
  - a lot easier if files produced by chainsaw contain references to the original event
- Label produced dataset with true/false positive
- Include syslog events for suricata alerts?