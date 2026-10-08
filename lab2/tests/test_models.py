from lab.models import Student


def test_student_average_calculation():
    s = Student(id=1, name="Тест", grades=[100, 90, None])
    assert s.average == 95.0


def test_student_average_empty_grades():
    s = Student(id=2, name="Тест 2", grades=[None, None])
    assert s.average == 0.0


def test_student_average_no_grades():
    s = Student(id=3, name="Тест 3", grades=[])
    assert s.average == 0.0