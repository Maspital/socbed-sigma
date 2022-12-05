import label_sigma
import pytest
import zipfile
import pathlib
import os


def clean_up(file):
    try:
        os.remove(file)
    except OSError:
        pass


class TestLabeling:
    log_sources = [
        "winlogbeat"
        # suricata, sysmon, etc
    ]

    _test_data_dir = pathlib.Path(__file__).resolve().parent.joinpath("test_data")
    _repo_root_dir = pathlib.Path(__file__).resolve().parents[3]

    @pytest.mark.parametrize("log_source", log_sources)
    def test_labeling_produces_desired_result(self, log_source, capfd):
        full_logfile_path, full_rule_dict_path = self.get_testing_data(log_source)
        expected_output = self.get_expected_output(log_source)
        logfile, rules_dict = label_sigma.open_json_files(full_logfile_path, full_rule_dict_path)

        label_sigma.label_alerts(logfile, rules_dict)
        clean_up(full_logfile_path)

        actual_out, error = capfd.readouterr()
        assert expected_output in actual_out

    def get_testing_data(self, log_source):
        sim_filename = "EntireSimulation_" + log_source + "_sigma.json"
        self.prepare_test_data(sim_filename[:-5])
        full_logfile_path = self._test_data_dir.joinpath(sim_filename)

        full_rule_dict_path = self._repo_root_dir.joinpath("labeling_metadata/rule_dict.json")

        return full_logfile_path, full_rule_dict_path

    def prepare_test_data(self, filename):
        archive = self._test_data_dir.joinpath(filename + ".zip")
        with zipfile.ZipFile(archive, "r") as zip_file:
            zip_file.extractall(self._test_data_dir)

    def get_expected_output(self, log_source):
        expected = self._test_data_dir.joinpath("expected_" + log_source + "_hits")
        with open(expected) as file:
            expected_out = file.read()
            return expected_out
