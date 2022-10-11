import label_sigma
import re


def test_convert_string_to_regex_pattern():
    string_1 = "cmd.exe /c echo ANY_WORD_CHAR > \\\\.\\pipe\\ANY_WORD_CHAR"
    expected_pattern_1 = re.compile(r"cmd\.exe /c echo \w+ > \\\\\.\\pipe\\\w+")
    pattern_1 = label_sigma.convert_string_to_regex_pattern(string_1)
    assert pattern_1 == expected_pattern_1

    string_2 = ("schtasks  /create /sc once /st 23:59 /tn ANY_WORD_CHAR "
                "/tr C:\\Windows\\meterpreter_bind_tcp.exe /ru BREACH\\client1")
    expected_pattern_2 = re.compile(r"schtasks  /create /sc once /st 23:59 /tn \w+ "
                                    r"/tr C:\\Windows\\meterpreter_bind_tcp\.exe /ru BREACH\\client1")
    pattern_2 = label_sigma.convert_string_to_regex_pattern(string_2)
    assert pattern_2 == expected_pattern_2
