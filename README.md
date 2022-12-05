# SOCBED-Sigma
This plugin is intended to extend the functionality of the [SOCBED framework](https://github.com/fkie-cad/socbed)
by enabling the user to generate datasets of [Sigma](https://github.com/SigmaHQ/sigma)-alerts in a reproducible manner, 
and then automatically label the contents of those datasets as true or false positives.
The labeled datasets could then be used for further research.

_[Using Sigma rules v0.22, changing may break labeling]_

## Prerequisites
- Configure and build SOCBED as described in the base [SOCBED repository](https://github.com/fkie-cad/socbed)

Further instructions assume that your _**current directory is the base directory of this README**_.
- Install additional dependencies in your SOCBED virtual environment (that you created while installing SOCBED)
    ```shell
    source ~/.virtualenvs/socbed/bin/activate
    pip install elasticsearch elasticsearch-dsl
    ```
- Download and extract [Chainsaw](https://github.com/WithSecureLabs/chainsaw) v2.3.0
    ```shell
  wget -O chainsaw.tar.gz https://github.com/WithSecureLabs/chainsaw/releases/download/v2.3.0/chainsaw_x86_64-unknown-linux-gnu.tar.gz
  tar -xf chainsaw.tar.gz
  mv chainsaw/chainsaw src/
  rm -rf chainsaw* # we only need the binary
    ```
- Install SOCBED-Sigma in your virtual environment
    ```shell
  pip install --editable .
    ```
After finishing the steps above, run `tox` and `socbed_sigma -h` to verify correct installation.


## Generating datasets
This process will take approximately 120 minutes.
```shell
source ~/.virtualenvs/socbed/bin/activate
socbed_sigma --generate
```
Afterwards, you will find another directory named after the starting time of your simulation (note that all times are UTC).
Therein, you will find several `*_winlogbeat.jsonl` files containing all logs produced by SOCBED clients during a given time;
once for the entire simulation, and once for each attack.


## Processing a dataset
Process the generated dataset using chainsaw and Sigma by running
```shell
source ~/.virtualenvs/socbed/bin/activate
socbed_sigma --label /path/to/your/dataset/

# for example:
# socbed_sigma --label ./2022-09-23T09_35_12Z
```
After execution has finished, the dataset directory will contain two additional files per `*_winlogbeat.jsonl`:
- `*_sigma.txt`, containing generated Sigma alerts from the log file of the same name in human-readable form
- `*_sigma.json`, containing generated Sigma alerts from the log file of the same name in json format for further processing


## Labeling a dataset
Evaluate and label the created Sigma alerts for a single file by running
```shell
source ~/.virtualenvs/socbed/bin/activate
socbed_sigma --label /path/to/your/sigma.json

# for example:
# socbed_sigma --label ./2022-09-23T09_35_12Z/EntireSimulation_sigma.json
```
The example above would produce the file `EntireSimulation_sigma_LABELED.json`.
It contains a JSON array, with each item having the following fields of interest:
- `rule`: Contains the full name of the triggered Sigma rule (string)
- `metadata.misuse`: Labels the alert as true or false positive (bool)
- `event`: Contains the original event from winlogbeat the Sigma rule triggered on (dict)
