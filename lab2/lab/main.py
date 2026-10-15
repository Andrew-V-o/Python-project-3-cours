import sys
from typing import List, Optional
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

DEFAULT_CSV_PATH = "data/students.csv"


def format_student_table(students: List[Student]) -> str:
    """Формирует текстовую таблицу с фиксированной шириной колонок."""
    if not students:
        return "Список студентов пуст."
        
    max_grades_count = max((len(s.grades) for s in students), default=0)
    
    id_width = max(len("ID"), max(len(str(s.id)) for s in students))
    name_width = max(len("ФИО"), max(len(s.name) for s in students))
    avg_width = max(len("Ср. балл"), 8)
    grade_col_width = 6
    
    header_id = "ID".ljust(id_width)
    header_name = "ФИО".ljust(name_width)
    header_avg = "Ср. балл".rjust(avg_width)
    
    grade_headers = [f"Отм.{i+1}".rjust(grade_col_width) for i in range(max_grades_count)]
    header_grades = " ".join(grade_headers) if grade_headers else "Оценки"
    
    header_line = f"| {header_id} | {header_name} | {header_avg} | {header_grades} |"
    separator = "-" * len(header_line)
    lines = [separator, header_line, separator]
    
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


def input_grades_interactive() -> List[Optional[int]]:
    """Запрашивает у пользователя оценки и парсит их."""
    print("Введите оценки через запятую/пробел. Пустая отметка: '-' или пробел.")
    print("Пример: 85, -, 90, 100")
    raw_input = input("Оценки: ").strip()
    return parse_grades_input(raw_input)


def print_menu(current_file: Optional[str]):
    print("\n" + "="*40)
    if current_file:
        print(f"  Текущий файл: {current_file}")
    else:
        print("  Данные загружены в память (файл не выбран)")
    print("="*40)
    print("  МЕНЮ УПРАВЛЕНИЯ СТУДЕНТАМИ")
    print("1. Загрузить из CSV")
    print("2. Сохранить в CSV")
    print("3. Показать всех студентов (таблица)")
    print("4. Добавить студента")
    print("5. Удалить студента по ID")
    print("6. Обновить оценки по ID")
    print("7. Показать статистику по группе")
    print("8. Экспорт ТОП-N студентов в CSV")
    print("9. Сортировка списка")
    print("0. Выход")


def main():
    students: List[Student] = []
    current_filepath: Optional[str] = None

    while True:
        print_menu(current_filepath)
        choice = input("Выберите пункт меню: ").strip()
        
        try:
            if choice == "1":
                filepath = input(f"Введите путь к CSV (по умолчанию {DEFAULT_CSV_PATH}): ").strip()
                if not filepath:
                    filepath = DEFAULT_CSV_PATH
                students = load_students_from_csv(filepath)
                current_filepath = filepath
                print(f"Успешно загружено студентов: {len(students)} из '{filepath}'")
                
            elif choice == "2":
                if not students:
                    print("Нечего сохранять: список студентов пуст.")
                    continue
                filepath = input(f"Введите путь для сохранения (по умолчанию {current_filepath or DEFAULT_CSV_PATH}): ").strip()
                if not filepath:
                    filepath = current_filepath or DEFAULT_CSV_PATH
                save_students_to_csv(filepath, students)
                current_filepath = filepath
                print(f"Данные успешно сохранены в '{filepath}'.")
                
            elif choice == "3":
                print("\n" + format_student_table(students))
                
            elif choice == "4":
                student_id = int(input("Введите ID студента (целое число): ").strip())
                name = input("Введите ФИО студента: ").strip()
                grades = input_grades_interactive()
                
                add_student(students, student_id, name, grades)
                
                if current_filepath:
                    save_students_to_csv(current_filepath, students)
                    print(f"Студент '{name}' добавлен. Изменения сохранены в '{current_filepath}'.")
                else:
                    print(f"Студент '{name}' добавлен в память. (Не забудьте сохранить через п.2)")
                    
            elif choice == "5":
                student_id = int(input("Введите ID студента для удаления: ").strip())
                removed = remove_student(students, student_id)
                
                if current_filepath:
                    save_students_to_csv(current_filepath, students)
                    print(f"Студент '{removed.name}' удален. Изменения сохранены.")
                else:
                    print(f"Студент '{removed.name}' удален из памяти.")
                    
            elif choice == "6":
                student_id = int(input("Введите ID студента для обновления оценок: ").strip())
                new_grades = input_grades_interactive()
                
                updated = update_student_grades(students, student_id, new_grades)
                
                if current_filepath:
                    save_students_to_csv(current_filepath, students)
                    print(f"Оценки студента '{updated.name}' обновлены. Файл сохранен.")
                else:
                    print(f"Оценки студента '{updated.name}' обновлены в памяти.")
                    
            elif choice == "7":
                stats = get_group_stats(students)
                print("\n--- Статистика по группе ---")
                print(f"Всего студентов:   {stats['count']}")
                print(f"Общий средний балл: {stats['overall_avg']:.2f}")
                if stats["best"]:
                    print(f"Лучший студент: {stats['best'].name} (Ср. балл: {stats['best'].average:.2f})")
                    print(f"Худший студент: {stats['worst'].name} (Ср. балл: {stats['worst'].average:.2f})")
                    
            elif choice == "8":
                n = int(input("Введите количество студентов (N): ").strip())
                filepath = input("Введите путь для сохранения файла ТОП-N: ").strip()
                top_list = get_top_n_students(students, n)
                export_top_n_to_csv(filepath, top_list)
                print(f"ТОП-{len(top_list)} студентов экспортированы в '{filepath}'.")
                
            elif choice == "9":
                print("Критерии сортировки: avg (средний балл), name (ФИО), id (ID)")
                by = input("Выберите критерий [по умолчанию avg]: ").strip().lower() or "avg"
                students = sort_students(students, by=by)
                print("Список отсортирован.")
                print(format_student_table(students))
                
            elif choice == "0":
                print("Завершение работы программы. До свидания!")
                sys.exit(0)
                
            else:
                print("Некорректный пункт меню. Попробуйте снова.")
                
        except StudentAppError as e:
            print(f"\n[Ошибка приложения]: {e}")
        except ValueError as e:
            print(f"\n[Ошибка ввода]: Ожидалось число или корректный формат данных. ({e})")
        except FileNotFoundError:
            print(f"\n[Ошибка файла]: Файл не найден. Проверьте путь.")
        except PermissionError:
            print(f"\n[Ошибка доступа]: Нет прав для чтения/записи файла.")
        except Exception as e:
            print(f"\n[Непредвиденная ошибка]: {e}")


if __name__ == "__main__":
    main()