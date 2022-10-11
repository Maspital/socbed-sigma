import helper
import re


def test_print_with_timestamp(capfd):
    expected_out = re.compile(
        r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\d\d\d\dZ: some text here\n")
    helper.print_with_timestamp("some text here")
    out, err = capfd.readouterr()
    out = helper.remove_ansi_escapes(out)
    assert expected_out.match(out) is not None


def test_get_iso_time():
    time_in_seconds = 1665146640
    expected_iso_time = "2022-10-07T12:44:00Z"
    resulting_iso_time = helper.get_iso_time(time_in_seconds)
    assert resulting_iso_time == expected_iso_time


def test_get_epoch():
    out = helper.get_epoch()
    digits = len(str(out))
    # note: above a certain number length (~10**12), using log10 is way faster, but may
    # actually output incorrect results due to rounding errors for certain numbers
    # digits = int(math.log10(out))+1
    assert digits == 10


def test_extend_filename():
    original_filename = "/some/path/some_file.type"
    expected_filename = "/some/path/some_file_with_a_suffix.type"
    resulting_filename = helper.extend_filename(original_filename, "with_a_suffix")
    assert resulting_filename == expected_filename


def test_remove_ansi_escapes():
    original_text = "\033[1mThis text should be bold!\033[0m"
    expected_out = "This text should be bold!"
    out = helper.remove_ansi_escapes(original_text)
    assert out == expected_out
