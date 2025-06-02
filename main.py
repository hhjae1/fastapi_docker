from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# 학점 -> 점수 매핑
grade_to_score = {
    "A+": 4.5, "A": 4.0,
    "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0,
    "D+": 1.5, "D": 1.0,
    "F": 0.0
}

# 과목 모델
class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str = Field(..., pattern="^(A\\+|A|B\\+|B|C\\+|C|D\\+|D|F)$")

# 학생 모델
class Student(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

# POST /score API
@app.post("/score")
def calculate_score(data: Student):
    total_score = 0.0
    total_credits = 0

    for course in data.courses:
        score = grade_to_score[course.grade]
        total_score += score * course.credits
        total_credits += course.credits

    if total_credits == 0:
        raise HTTPException(status_code=400, detail="No valid courses")

    gpa = round(total_score / total_credits + 1e-8, 2)

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
