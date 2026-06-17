from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()

class student(BaseModel):
    id: int
    name: str
    age: int
    marks: int
    grade: str

students = {
    1: {"name": "Alice", "age": 20,"marks":80, "grade": "A+"},
    2: {"name": "Bob", "age": 22, "marks": 70, "grade": "B"},
    3: {"name": "Charlie", "age": 19, "marks": 60, "grade": "C"},
}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    student = students.get(student_id)
    if student:
        return {"student_id": student_id, "name": student["name"], "age": student["age"], "marks": student["marks"], "grade": student["grade"]}
    else:
        return {"error": "Student not found"}
    
@app.post("/students")
def create_student(student: student):
    if student.id in students:
        raise HTTPException(status_code=400, detail="Student with this ID already exists")
    students[student.id] = {"name": student.name, "age": student.age, "marks": student.marks, "grade": student.grade}
    return {"message": "Student created successfully", "student_id": student.id}