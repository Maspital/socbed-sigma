import label_sigma
import re

mock_sigma_alert_1 = {"rule": "Rule name one",
                      "key1": "Some random content",
                      "key2": {
                          "key2-1": "Some random content",
                          "key2-2": "Specific content and some qwer1234 gibberish"
                      }}
mock_sigma_alert_2 = {"rule": "Rule name two",
                      "key1": "Some random field"}


def test_is_true_positive():
    mock_rule_dict = {
        "Rule name one": {
            "conditions": {
                "entry1": [
                    "some_key.another_key",
                    "Some desired content"
                ],
                "entry2": [
                    "key2.key2-2",
                    r"Specific content and some \w+ gibberish"
                ]
            }
        },
        "Rule name two": {
            "conditions": {
                "entry1": [
                    "some_key.another_key",
                    r"Some desired content"
                ]
            }
        }
    }

    assert label_sigma.is_true_positive(sigma_alert=mock_sigma_alert_1,
                                        rule="Rule name one",
                                        rules_dict=mock_rule_dict)
    assert not label_sigma.is_true_positive(sigma_alert=mock_sigma_alert_2,
                                            rule="Rule name two",
                                            rules_dict=mock_rule_dict)


def test_condition_is_met():
    condition_1 = [
        "some_key.another_key",
        r"These are not the droids you're looking for"
    ]
    condition_2 = [
        "key2.key2-2",
        r"Specific content and some \w+ gibberish"
    ]

    assert not label_sigma.condition_is_met(sigma_alert=mock_sigma_alert_1,
                                            condition=condition_1)
    assert label_sigma.condition_is_met(sigma_alert=mock_sigma_alert_1,
                                        condition=condition_2)


def test_convert_string_to_regex_pattern():
    string_1 = "cmd.exe /c echo ANY_WORD_CHARS > \\\\.\\pipe\\ANY_WORD_CHARS"
    expected_pattern_1 = re.compile(r"cmd\.exe /c echo \w+ > \\\\\.\\pipe\\\w+")
    pattern_1 = label_sigma.convert_string_to_regex_pattern(string_1)
    assert pattern_1 == expected_pattern_1

    string_2 = ("schtasks /create /sc once /st 23:59 /tn ANY_WORD_CHARS "
                "/tr C:\\Windows\\meterpreter_bind_tcp.exe /ru BREACH\\client1")
    expected_pattern_2 = re.compile(r"schtasks /create /sc once /st 23:59 /tn \w+ "
                                    r"/tr C:\\Windows\\meterpreter_bind_tcp\.exe /ru BREACH\\client1")
    pattern_2 = label_sigma.convert_string_to_regex_pattern(string_2)
    assert pattern_2 == expected_pattern_2


def test_label_alert():
    some_sigma_alert = {}
    expected_dict = {"metadata": {"misuse": True}}
    label_sigma.apply_label(some_sigma_alert, True)
    assert expected_dict == some_sigma_alert


def test_rename_fields():
    some_sigma_alert = {
        "document": {
            "some_key": "other data",
            "data": {
                "some_key": "some_value",
                "another_key": ["a", "list"]
            },
        },
        "name": "Rule name"
    }
    expected_dict = {
        "document": {
            "some_key": "other data"
        },
        "event": {
            "some_key": "some_value",
            "another_key": ["a", "list"]
        },
        "rule": "Rule name"
    }
    label_sigma.rename_fields(some_sigma_alert)
    assert expected_dict == some_sigma_alert
