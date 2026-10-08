import pytest
from lab.io_utils import (
    parse_grade,
    parse_grades_input,
    load_students_from_csv,
    save_students_to_csv,
)
from lab.errors import ValidationError


def test_parse_grade_valid():
    assert parse_grade("85") == 85
    assert parse_grade("-") is None
    assert parse_grade("") is None


def test_parse_grade_invalid():
    with pytest.raises(ValidationError):
        parse_grade("150")
    with pytest.raises(ValidationError):
        parse_grade("abc")


def test_parse_grades_input_with_empty_values():
    result = parse_grades_input("85, -, none, 90")
    assert result == [85, None, None, 90]


def test_csv_roundtrip(tmp_path, sample_students):
    file_path = tmp_path / "test_students.csv"
    save_students_to_csv(str(file_path), sample_students)
    
    loaded = load_students_from_csv(str(file_path))
    assert len(loaded) == len(sample_students)
    assert loaded[0].id == sample_students[0].id
    assert loaded[0].grades == sample_students[0].grades