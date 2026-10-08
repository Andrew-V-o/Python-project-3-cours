from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Student:
    id: int
    name: str
    grades: List[Optional[int]] = field(default_factory=list)

    @property
    def average(self) -> float:
        """Возвращает средний балл по существующим оценкам.
         Если оценок нет или все пустые, возвращает 0.0.
        """
        valid_grades = [g for g in self.grades if g is not None]
        if not valid_grades:
            return 0.0
        return round(sum(valid_grades) / len(valid_grades), 2)