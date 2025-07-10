import uvicorn as uv
from fastapi import FastAPI as fapi, Path as pth, Query as qry, HTTPException, Body as bd
from pydantic import BaseModel as Bsm, Field as fld, validator as vld
from enum import Enum as enm
import json


app = fapi()

filename = "students.jsonl"

#saving in file
def saveData(data: dict, filemane="filename"):
    with open(filemane, "a", encoding="utf-8") as f:
        json.dump(data, f)
        f.write("\n")

HOST = "127.0.0.1"
PORT = 6060

class Gender(str, enm):
    male = "M"
    female = "F"

class Student(Bsm):
    name: str 
    roll: str
    age: int = fld(...)
    add: str | None = None
    gender : Gender

    @vld("name")
    def make_first_capital(cls, value: str) -> str:
        value = value.strip()
        if not value:
          raise ValueError("Name cannot be empty or just whitespace")
        return value[0].upper() + value[1:]
    
    @vld("age")
    def check_age(cls, val: int) -> int:
        if val < 18:
            raise ValueError("Age should be greater than 18")
        return val

@app.on_event("startup")
async def on_startup():
    print(f"Successfully connected on path: http://{HOST}:{PORT}")



@app.post("/createStudent/")
async def create_Student(student: Student):
        
        student_data = student.dict()
        saveData(student_data)
        # return {"msg": "Person registered", "data": student}
        return {
        "message": "Student data saved to file",
        "data": student_data
    }

@app.get("/getAllStudents/")
def returnData():
    students = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    students.append(json.loads(line))
    except FileNotFoundError:
        return {"message":'No data found. File does not exist'}
    
    return {"message" : f"{len(students)} students loaded", "students" : students}

@app.get("/getOneStudent/")
async def getStudent(roll:str = qry(None), name: str = qry(None)):
    if not roll and not name:
        raise HTTPException(status_code=400, detail="Either roll or name must be provided")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                student = json.loads(line.strip())

                if (roll and student.get("roll","").lower() == roll.lower()) or \
                   (name and student.get("name", "").lower() == name.lower()):
                    return {"message": "Student found", "student": student}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Student file not found")
    
    raise HTTPException(status_code=404, detail="No student found with the given details")

@app.patch("/patchStudent/")
async def patchingStudent( updates: dict = bd(...),roll:str = qry(None) , name:str = qry(None)):
    
    updated = False
    upded_stds = []
    if not roll and not name:
        raise HTTPException(status_code=400, detail = "Either roll or name must be given")
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                student = json.loads(line.strip())

                if ((roll and student.get("roll","").lower() == roll.lower()) or \
                   (name and student.get("name","").lower() == name.lower())):
                    for key, val in updates.items():
                        if key in student and val is not None:
                            student[key] = val
                    updated = True
                upded_stds.append(student)
                    
        if not updated:
            raise ValueError(f"No student found with the given details")
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Student data file not found")
    
    with open(filename, "w", encoding="utf-8") as f:
        for student in upded_stds:  
            json.dump(student, f)
            f.write("\n")

    return {"message" : "Student updated successfully with PATCH, use GET for veryfying"}  

@app.delete("/deleteStudent")
async def delStudent(roll:str = qry(None) , name:str = qry(None)):
    deld = None
    found = False
    remaining = []

    if not name and not roll:
        raise HTTPException(status_code=400, detail="Either name or rol must be provided")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                student = json.loads(line.strip())

                if (roll and student.get("roll","").lower() == roll.lower()) or \
                   (name and student.get("name","").lower() == name.lower()):
                    found = True
                    deld = student
                    continue
                remaining.append(student)
        if not found:
            raise HTTPException(status_code=404, detail="No student dound with the given details")
        
        with open(filename, "w", encoding="utf-8") as f:
                for stds in remaining:
                    json.dump(stds, f)
                    f.write("\n")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Student data file not found")
    
    return {"message" : "student deleted successfully", "Deleted student" : deld}
if __name__ == "__main__":
    uv.run("myApp1:app", host=HOST, port= PORT, reload=True, log_level="debug")
    
