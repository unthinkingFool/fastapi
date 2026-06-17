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
  
    
@app.post("/students")
def submit_marks(student: student):
    if student.id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if student.marks < 0 or student.marks > 100:
        raise HTTPException(status_code=400, detail="Marks must be between 0 and 100 , but got {}".format(student.marks))
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    students[student.id] = {"name": student.name, "age": student.age, "marks": student.marks, "grade": student.grade}
    return {"message": "Student marks submitted successfully", "student_id": student.id, "name": student.name, "age": student.age, "marks": student.marks, "grade": student.grade}