class StudentAppError(Exception):
    """Базовое исключение для приложения управления студентами."""
    pass


class StudentNotFoundError(StudentAppError):
    """Вызывается, если студент с данным ID не найден."""
    pass


class DuplicateIdError(StudentAppError):
    """Вызывается при попытке создать студента с уже существующим ID."""
    pass


class ValidationError(StudentAppError):
    """Вызывается при невалидных данных (неверный диапазон оценок, пустое имя и т.д.)."""
    pass


class CSVFormatError(StudentAppError):
    """Вызывается при ошибке структуры или парсинга CSV файла."""
    pass