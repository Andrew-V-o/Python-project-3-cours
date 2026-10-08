from typing import List, Optional, Dict, Any
from lab.models import Student
from lab.errors import StudentNotFoundError, DuplicateIdError, ValidationError


def add_student(students: List[Student], student_id: int, name: str, grades: List[Optional[int]]) -> Student:
    """Добавляет нового студента в список."""
    if any(s.id == student_id for s in students):
        raise DuplicateIdError(f"Студент с ID {student_id} уже существует.")
    if not name.strip():
        raise ValidationError("Имя студента не может быть пустым.")
    
    student = Student(id=student_id, name=name.strip(), grades=grades)
    students.append(student)
    return student


def remove_student(students: List[Student], student_id: int) -> Student:
    """Удаляет студента по ID."""
    for i, student in enumerate(students):
        if student.id == student_id:
            return students.pop(i)
    raise StudentNotFoundError(f"Студент с ID {student_id} не найден.")


def update_student_grades(students: List[Student], student_id: int, new_grades: List[Optional[int]]) -> Student:
    """Обновляет оценки студента по ID (поддерживает пустые отметки None)."""
    for student in students:
        if student.id == student_id:
            student.grades = new_grades
            return student
    raise StudentNotFoundError(f"Студент с ID {student_id} не найден.")


def sort_students(students: List[Student], by: str = "avg") -> List[Student]:
    """Сортирует список студентов по заданному критерию:
    - 'avg': по убыванию среднего балла, затем по имени (a..z);
    - 'name': по имени (a..z);
    - 'id': по возрастанию id.
    """
    if by == "avg":
        return sorted(students, key=lambda s: (-s.average, s.name.lower()))
    elif by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    elif by == "id":
        return sorted(students, key=lambda s: s.id)
    else:
        raise ValidationError(f"Неизвестный параметр сортировки: {by}")


def get_group_stats(students: List[Student]) -> Dict[str, Any]:
    """Возвращает общую статистику по группе."""
    if not students:
        return {
            "count": 0,
            "overall_avg": 0.0,
            "best": None,
            "worst": None
        }

    all_grades = [g for s in students for g in s.grades if g is not None]
    overall_avg = round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    sorted_by_avg = sort_students(students, by="avg")
    
    return {
        "count": len(students),
        "overall_avg": overall_avg,
        "best": sorted_by_avg[0],
        "worst": sorted_by_avg[-1]
    }


def get_top_n_students(students: List[Student], n: int) -> List[Student]:
    """Возвращает TOP-N студентов по среднему баллу."""
    sorted_list = sort_students(students, by="avg")
    return sorted_list[:max(0, n)]