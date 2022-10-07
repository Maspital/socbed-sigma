import helper


def test_print_with_timestamp():
    pass


def test_get_iso_time():
    time_in_seconds = 1665146640
    expected_iso_time = "2022-10-07T12:44:00Z"
    resulting_iso_time = helper.get_iso_time(time_in_seconds)
    assert resulting_iso_time == expected_iso_time


def test_get_epoch():
    pass


def test_extend_filename():
    original_filename = "/some/path/some_file.type"
    expected_filename = "/some/path/some_file_with_a_suffix.type"
    resulting_filename = helper.extend_filename(original_filename, "with_a_suffix")
    assert resulting_filename == expected_filename
