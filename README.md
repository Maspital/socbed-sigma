# SOCBED-SIGMA
This plugin is intended to extend the functionality of the [SOCBED framework](https://github.com/fkie-cad/socbed)
by enabling the user to generate datasets of [SIGMA](https://github.com/SigmaHQ/sigma)-alerts in a reproducible manner, 
and then automatically label the contents of those datasets as true or false positives.
The labeled datasets could then be used for further research.

_[Using SIGMA rules v0.22, changing may break labeling]_

## Prerequisites
- Configure and build SOCBED as described in the base [SOCBED repository](https://github.com/fkie-cad/socbed)

Further instructions assume that your _**current directory is the base directory of this repository**_.
- Install additional dependencies in your SOCBED virtual environment (that you created while installing SOCBED)
    ```shell
    source ~/.virtualenvs/socbed/bin/activate
    pip install elasticsearch elasticsearch-dsl
    ```
- Download and extract [Chainsaw](https://github.com/WithSecureLabs/chainsaw) v2.1.0
    ```shell
  wget -O chainsaw.tar.gz https://github.com/WithSecureLabs/chainsaw/releases/download/v2.1.0/chainsaw_x86_64-unknown-linux-gnu.tar.gz
  tar -xf chainsaw.tar.gz
  mv chainsaw/chainsaw src/
  rm -rf chainsaw* # we only need the binary
    ```


## Generating datasets
This process will take approximately 125 minutes.
```shell
source ~/.virtualenvs/socbed/bin/activate
./generate_dataset
```
Afterwards, you will find another directory named after the starting time of your simulation (note that all times are UTC).
Therein, you will find three types of files, once for each attack and once for the entire simulation:
- `*_winlogbeat.jsonl`, containing all logs produced by SOCBED clients during a given time
- `*_sigma.txt`, containing generated SIGMA alerts from the log-file of the same name in human-readable form
- `*_sigma.json`, containing generated SIGMA alerts from the log-file of the same name in json format for further processing


## Labeling a dataset
Evaluate and label the created SIGMA alerts for a single file by running
```shell
source ~/.virtualenvs/socbed/bin/activate
./label_dataset <sim_id>/<attack>_sigma.jsonl

# for example:
# ./label_dataset 2022-09-23T09_35_12Z/EntireSimulation_sigma.json
```
The example above would produce the file `EntireSimulation_sigma_LABELED.json`.
It contains a JSON array, with each item having the following fields of interest:
- `rule`: Contains the full name of the triggered SIGMA rule (string)
- `metadata.misuse`: Labels the alert as true or false positive (bool)
- `event`: Contains the original event from winlogbeat the SIGMA rule triggered on (dict)

## TODO
- Further examine the labeling process of generated datasets and make adjustments where appropriate
