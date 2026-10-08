import pytest
from lab.models import Student
from lab.errors import DuplicateIdError, StudentNotFoundError, ValidationError
from lab.processing import (
    add_student,
    remove_student,
    update_student_grades,
    sort_students,
    get_group_stats,
    get_top_n_students,
)


def test_add_student_success(sample_students):
    s = add_student(sample_students, 6, "Новый Студент", [90, 95])
    assert s.id == 6
    assert len(sample_students) == 6


def test_add_student_duplicate_id(sample_students):
    with pytest.raises(DuplicateIdError):
        add_student(sample_students, 1, "Дубликат", [80])


def test_remove_student_success(sample_students):
    removed = remove_student(sample_students, 1)
    assert removed.id == 1
    assert len(sample_students) == 4


def test_remove_student_not_found(sample_students):
    with pytest.raises(StudentNotFoundError):
        remove_student(sample_students, 999)


def test_update_student_grades(sample_students):
    updated = update_student_grades(sample_students, 1, [100, None, 100])
    assert updated.grades == [100, None, 100]


def test_sort_students_by_avg(sample_students):
    sorted_list = sort_students(sample_students, by="avg")
    assert sorted_list[0].name == "Иванова Анна"


def test_get_group_stats(sample_students):
    stats = get_group_stats(sample_students)
    assert stats["count"] == 5
    assert stats["best"].name == "Иванова Анна"


def test_get_top_n_students(sample_students):
    top_2 = get_top_n_students(sample_students, 2)
    assert len(top_2) == 2
    assert top_2[0].name == "Иванова Анна"