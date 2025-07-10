# FastAPI_codes

A collection of FastAPI examples, utilities, and project code snippets for learning and building backend APIs with Python's FastAPI framework.
---
## 🔨 Tools and Sites
- [tutorialspoint](https://www.tutorialspoint.com/fastapi/index.htm)
- [FastAPI docs](https://fastapi.tiangolo.com/)
- Postman for endpoint testing and validation

---

## 🗃️ Modules
- Used fastapi module for REST structures
- Pydantic for request and response validation
- implemented file based storage in a json lines file (as seen "students.json")
- json for data parsing from and into requests and responses.
  
---

## 🔗 API Endpoints

- `POST /createStudent/` – Create and save a new student to the JSONL file
- `GET /getAllStudents/` – Retrieve all students from the file
- `GET /getOneStudent/?roll=...&name=...` – Fetch a student by roll number or name
- `PATCH /patchStudent/?roll=...&name=...` – Partially update a student's data using roll or name
- `DELETE /deleteStudent?roll=...&name=...` – Delete a student by roll number or name
