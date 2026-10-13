from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
from lab.io_utils import load_students_from_csv, save_students_to_csv
from lab.processing import add_student, remove_student, update_student_grades
from lab.models import Student

app = FastAPI()
CSV_PATH = "data/students.csv"

class StudentIn(BaseModel):
    id: int
    name: str
    grades: List[Optional[int]] = []

class GradesIn(BaseModel):
    grades: List[Optional[int]]

@app.get("/api/students")
def get_students():
    students = load_students_from_csv(CSV_PATH)
    return [{"id": s.id, "name": s.name, "average": s.average, 
             "grades": [g if g is not None else "-" for g in s.grades]} for s in students]

@app.post("/api/students")
def add_student_api(student: StudentIn):
    students = load_students_from_csv(CSV_PATH)
    add_student(students, student.id, student.name, student.grades)
    save_students_to_csv(CSV_PATH, students)
    return {"message": "Добавлен"}

@app.put("/api/students/{sid}")
def update_grades(sid: int, data: GradesIn):
    students = load_students_from_csv(CSV_PATH)
    update_student_grades(students, sid, data.grades)
    save_students_to_csv(CSV_PATH, students)
    return {"message": "Обновлено"}

@app.delete("/api/students/{sid}")
def delete_student(sid: int):
    students = load_students_from_csv(CSV_PATH)
    remove_student(students, sid)
    save_students_to_csv(CSV_PATH, students)
    return {"message": "Удален"}

@app.get("/", response_class=HTMLResponse)
def get_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()