from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI()

grade_map = {
    "A+": 4.5,
    "A": 4.0,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/student_summary")
async def calculate_summary(data: StudentRequest):
    total_credits = 0
    total_points = Decimal("0.0")

    for course in data.courses:
        credit = course.credits
        grade = grade_map.get(course.grade, 0.0)
        total_credits += credit
        total_points += Decimal(str(credit * grade))

    # 소수점 셋째 자리에서 반올림 (ROUND_HALF_UP)
    gpa = Decimal(total_points / total_credits).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": float(gpa),  # Swagger 문서에서 보기 좋게 숫자로 반환
            "total_credits": total_credits
        }
    }
