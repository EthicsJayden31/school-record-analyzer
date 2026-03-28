import pytest

from school_record_analyzer.drive import build_drive_download_url, extract_drive_file_id
from school_record_analyzer.parser import parse_record_file


def test_extract_drive_file_id_from_file_path_url():
    url = "https://drive.google.com/file/d/1AbCdEfGhIJklMNop/view?usp=sharing"
    assert extract_drive_file_id(url) == "1AbCdEfGhIJklMNop"


def test_extract_drive_file_id_from_query_url():
    url = "https://drive.google.com/open?id=xyz123_ABC"
    assert extract_drive_file_id(url) == "xyz123_ABC"


def test_build_download_url():
    assert build_drive_download_url("abc") == "https://drive.google.com/uc?export=download&id=abc"


def test_parser_rejects_non_google_url():
    with pytest.raises(ValueError):
        parse_record_file("https://example.com/file.txt")
