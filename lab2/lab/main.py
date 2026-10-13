import sys
from typing import List
from lab.models import Student
from lab.errors import StudentAppError
from lab.io_utils import (
    load_students_from_csv,
    save_students_to_csv,
    export_top_n_to_csv,
    parse_grades_input
)
from lab.processing import (
    add_student,
    remove_student,
    update_student_grades,
    sort_students,
    get_group_stats,
    get_top_n_students
)


def format_student_table(students: List[Student]) -> str:
    """Формирует текстовую таблицу с фиксированной шириной колонок.
    Пустые отметки обозначаются прочерком (-).
    """
    if not students:
        return "Список студентов пуст."

    max_grades_count = max((len(s.grades) for s in students), default=0)
    
    # Определение ширины основных столбцов
    id_width = max(len("ID"), max(len(str(s.id)) for s in students))
    name_width = max(len("ФИО"), max(len(s.name) for s in students))
    avg_width = max(len("Ср. балл"), 8)
    grade_col_width = 6

    # Формирование заголовка таблицы
    header_id = "ID".ljust(id_width)
    header_name = "ФИО".ljust(name_width)
    header_avg = "Ср. балл".rjust(avg_width)
    
    grade_headers = [f"Отм.{i+1}".rjust(grade_col_width) for i in range(max_grades_count)]
    header_grades = " ".join(grade_headers) if grade_headers else "Оценки"

    header_line = f"| {header_id} | {header_name} | {header_avg} | {header_grades} |"
    separator = "-" * len(header_line)

    lines = [separator, header_line, separator]

    # Заполнение строк данных
    for s in students:
        id_str = str(s.id).ljust(id_width)
        name_str = s.name.ljust(name_width)
        avg_str = f"{s.average:.2f}".rjust(avg_width)

        formatted_grades = []
        for i in range(max_grades_count):
            if i < len(s.grades):
                g = s.grades[i]
                val = str(g) if g is not None else "-"
            else:
                val = "-"
            formatted_grades.append(val.rjust(grade_col_width))

        grades_str = " ".join(formatted_grades) if formatted_grades else "-"
        lines.append(f"| {id_str} | {name_str} | {avg_str} | {grades_str} |")

    lines.append(separator)
    return "\n".join(lines)


def print_menu():
    print("\n=== Меню управления списком студентов ===")
    print("1. Загрузить из CSV")
    print("2. Сохранить в CSV")
    print("3. Показать всех студентов (таблица)")
    print("4. Добавить студента")
    print("5. Удалить студента по ID")
    print("6. Обновить оценки по ID (поддержка пустых отметок)")
    print("7. Показать статистику по группе")
    print("8. Экспорт ТОП-N студентов в CSV")
    print("9. Сортировка списка")
    print("0. Выход")


def main():
    students: List[Student] = []

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        try:
            if choice == "1":
                filepath = input("Введите путь к CSV файлу (например, data/students.csv): ").strip()
                students = load_students_from_csv(filepath)
                print(f"Успешно загружено студентов: {len(students)}")

            elif choice == "2":
                filepath = input("Введите путь для сохранения CSV: ").strip()
                save_students_to_csv(filepath, students)
                print("Данные успешно сохранены.")

            elif choice == "3":
                print("\nСписок студентов:")
                print(format_student_table(students))

            elif choice == "4":
                student_id = int(input("Введите ID студента (целое число): ").strip())
                name = input("Введите ФИО студента: ").strip()
                print("Введите оценки через запятую/пробел (для пустой отметки введите '-' или оставьте пробел):")
                grades_input = input("Оценки: ").strip()
                grades = parse_grades_input(grades_input)
                
                add_student(students, student_id, name, grades)
                save_students_to_csv("data/students.csv", students)
    
                print(f"Студент '{name}' с ID {student_id} успешно добавлен.")
                

            elif choice == "5":
                student_id = int(input("Введите ID студента для удаления: ").strip())
                removed = remove_student(students, student_id)
                print(f"Студент '{removed.name}' (ID {removed.id}) удален.")

            elif choice == "6":
                student_id = int(input("Введите ID студента для обновления оценок: ").strip())
                print("Введите новые оценки через запятую/пробел.")
                print("Пример ввода с пустыми отметками: 85, -, 90, -, 100")
                grades_input = input("Новые оценки: ").strip()
                new_grades = parse_grades_input(grades_input)
                
                updated = update_student_grades(students, student_id, new_grades)
                print(f"Оценки студента '{updated.name}' успешно обновлены.")

            elif choice == "7":
                stats = get_group_stats(students)
                print("\n--- Статистика по группе ---")
                print(f"Всего студентов: {stats['count']}")
                print(f"Общий средний балл: {stats['overall_avg']}")
                if stats["best"]:
                    print(f"Лучший студент: {stats['best'].name} (Ср. балл: {stats['best'].average})")
                if stats["worst"]:
                    print(f"Худший студент: {stats['worst'].name} (Ср. балл: {stats['worst'].average})")

            elif choice == "8":
                n = int(input("Введите количество студентов (N): ").strip())
                filepath = input("Введите путь для сохранения файла ТОП-N: ").strip()
                top_list = get_top_n_students(students, n)
                export_top_n_to_csv(filepath, top_list)
                print(f"ТОП-{len(top_list)} студентов успешно экспортированы в {filepath}.")

            elif choice == "9":
                print("Критерии сортировки: avg (средний балл), name (ФИО), id (ID)")
                by = input("Выберите критерий (avg/name/id) [по умолчанию avg]: ").strip().lower() or "avg"
                students = sort_students(students, by=by)
                print("Список отсортирован.")
                print(format_student_table(students))

            elif choice == "0":
                print("Завершение работы программы.")
                sys.exit(0)

            else:
                print("Некорректный пункт меню. Попробуйте снова.")

        except StudentAppError as e:
            print(f"\n[Ошибка приложения]: {e}")
        except ValueError as e:
            print(f"\n[Ошибка ввода]: Некорректный формат числа или данных ({e}).")
        except FileNotFoundError:
            print("\n[Ошибка]: Указанный файл не найден.")
        except Exception as e:
            print(f"\n[Непредвиденная ошибка]: {e}")


if __name__ == "__main__":
    main()