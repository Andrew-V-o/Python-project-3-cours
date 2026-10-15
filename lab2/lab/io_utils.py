import csv
from typing import List, Optional
from lab.models import Student
from lab.errors import CSVFormatError, ValidationError


def parse_grade(val: str) -> Optional[int]:
    """Парсит значение оценки. Возвращает None для пустой ячейки или прочерка."""
    val = val.strip()
    if not val or val == "-":
        return None
    try:
        grade = int(val)
        if not (0 <= grade <= 100):
            raise ValidationError(f"Оценка {grade} вне диапазона 0..100")
        return grade
    except ValueError:
        raise ValidationError(f"Некорректное значение оценки: '{val}'")


def parse_grades_input(input_str: str) -> List[Optional[int]]:
    """Преобразует введенную пользователем строку с оценками в список int | None."""
    if not input_str.strip():
        return []
    
    raw_tokens = input_str.split(",") if "," in input_str else input_str.split()
    grades = []
    
    for token in raw_tokens:
        token = token.strip().lower()
        if not token or token in ("-", "none", "null", "empty"):
            grades.append(None)
        else:
            try:
                g = int(token)
                if not (0 <= g <= 100):
                    raise ValidationError(f"Оценка {g} должна быть в диапазоне от 0 до 100.")
                grades.append(g)
            except ValueError:
                raise ValidationError(f"Недопустимое значение для оценки: '{token}'.")
    return grades


def load_students_from_csv(filepath: str) -> List[Student]:
    """Загружает список студентов из CSV файла."""
    students: List[Student] = []
    
    with open(filepath, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row and any(cell.strip() for cell in row)]
        
    if not rows:
        return students
        
    first_row = rows[0]
    if first_row and first_row[0].strip().lower() in ("id", "identifier"):
        rows = rows[1:]
        
    for row in rows:
        if len(row) < 2:
            raise CSVFormatError(f"Строка содержит менее двух обязательных колонок: {row}")
        try:
            student_id = int(row[0].strip())
        except ValueError:
            raise CSVFormatError(f"Некорректный ID студента: '{row[0]}'")
            
        name = row[1].strip()
        if not name:
            raise CSVFormatError("Имя студента не может быть пустым.")
            
        grades = [parse_grade(g) for g in row[2:]]
        students.append(Student(id=student_id, name=name, grades=grades))
        
    return students


def save_students_to_csv(filepath: str, students: List[Student]) -> None:
    """Сохраняет список студентов в CSV файл с выравниванием колонок оценок."""
    max_grades_len = max((len(s.grades) for s in students), default=0)
    header = ["id", "name"] + [f"grade{i+1}" for i in range(max_grades_len)]
    
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for s in students:
            padded_grades = [str(g) if g is not None else "" for g in s.grades]
            padded_grades.extend([""] * (max_grades_len - len(padded_grades)))
            row = [s.id, s.name] + padded_grades
            writer.writerow(row)


def export_top_n_to_csv(filepath: str, top_students: List[Student]) -> None:
    """Экспортирует ТОП-N студентов в CSV файл."""
    header = ["id", "name", "average", "grades"]
    
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for s in top_students:
            grades_str = " ".join(str(g) if g is not None else "-" for g in s.grades)
            writer.writerow([s.id, s.name, f"{s.average:.2f}", grades_str])