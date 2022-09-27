### Prerequisites
- Configure and build SOCBED as described in the base [SOCBED repository](https://github.com/fkie-cad/socbed)

Further instructions assume that your current directory is the base directory of this repository.
- Install additional dependencies in your SOCBED virtual environment (that you created while installing SOCBED)
    ```console
    source ~/.virtualenvs/socbed/bin/activate
    pip install elasticsearch elasticsearch-dsl
    ```
- Download and extract Chainsaw v2.1.0 (find more info about Chainsaw [here](https://github.com/WithSecureLabs/chainsaw))
    ```console
  wget -O chainsaw.tar.gz https://github.com/WithSecureLabs/chainsaw/releases/download/v2.1.0/chainsaw_x86_64-unknown-linux-gnu.tar.gz
  tar -xf chainsaw.tar.gz
  mv chainsaw/chainsaw src/
  rm -rf chainsaw* # we only need the binary
    ```


### Generating log files and alerts
This process will take approximately 65 minutes.
```console
source ~/.virtualenvs/socbed/bin/activate
./evaluate
```
Afterwards, you will find another directory named after the starting time of your simulation (note that all times are UTC).
Therein, you will find three types of files, once for each attack and once for the entire simulation:
- `*_winlogbeat.jsonl`, containing all logs produced by SOCBED clients during a given time
- `*_sigma.txt`, containing generated SIGMA alerts from the log-file of the same name in human-readable form
- `*_sigma.json`, containing generated SIGMA alerts from the log-file of the same name in json format for easier parsing


### Evaluate log files
Evaluate and label the created SIGMA alerts for a single file by running
```console
python src/label_sigma.py <sim_id>/<attack>_sigma.jsonl
# for example:
# python src/label_sigma.py 2022-09-23T09_35_12Z/EntireSimulation_sigma.json
```
This will produce labeled `.json` files you can use for training or similar purposes.

TODO
- Determine why the `Windows PowerShell Web Request` alert appears too often
- Ensure each expected alert actually originated from the expected source (an attack)
  - already mostly accomplished by checking certain fields
  - maybe extend by also looking at timestamps?
- Include syslog events for suricata alerts?