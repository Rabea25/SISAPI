# API Documentation

Complete reference for the University Student Information System API endpoints.

## Base URL
```
http://localhost:8000/
```

## Authentication

All endpoints (except public ones) require JWT authentication.

**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

**Get Token:**
```http
POST /auth/login/
{
  "username": "student_id",
  "password": "national_id"
}
```

---

## Authentication Endpoints

### POST /auth/login/
User authentication with JWT token generation.

**Request:**
```json
{
  "username": "20001",
  "password": "12345678901234"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Errors:**
- `401` - Invalid credentials

---

### POST /auth/refresh/
Refresh JWT access token.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### GET /auth/me/
Get current authenticated user information.

**Response (200):**
```json
{
  "message": "Token is authenticated.",
  "id": "20001",
  "name": "Alice Johnson"
}
```

---

## Student Endpoints

### GET /student/info/
Get complete student profile and academic standing.

**Response (200):**
```json
{
  "studentId": "20001",
  "nameEn": "Alice Johnson",
  "nameAr": "أليس جونسون",
  "email": "alice@university.edu",
  "level": 2,
  "earnedHours": 45,
  "passedCreditHours": 42,
  "cgpa": 3.4,
  "department": {
    "code": "CS",
    "name": "Computer Science",
    "description": "Department of Computer Science"
  },
  "currentSemester": "Fall",
  "currentAcademicYear": "2024-2025"
}
```

**Errors:**
- `404` - Student not found

---

### GET /student/grades/
Get complete academic transcript with all semesters and grades.

**Response (200):**
```json
{
  "studentId": "20001",
  "studentName": "Alice Johnson",
  "academicHistory": [
    {
      "yearId": 1,
      "yearName": "2024-2025",
      "semesters": [
        {
          "semesterId": 1,
          "semesterName": "Fall",
          "gpa": 3.2,
          "cgpa": 3.4,
          "registeredHours": 15,
          "earnedHours": 15,
          "enrollments": [
            {
              "courseCode": "CS101",
              "courseName": "Introduction to Programming",
              "credits": 3,
              "letterGrade": "A-",
              "numericGrade": 87.5,
              "coursework": 44,
              "exam": 43,
              "total": 87,
              "isPassed": true
            }
          ]
        }
      ]
    }
  ],
  "overallStats": {
    "totalCreditHours": 15,
    "passedCreditHours": 15,
    "overallCGPA": 3.4,
    "totalSemesters": 1
  }
}
```

---

### GET /student/current-semester/
Get current semester courses and grades (including incomplete).

**Response (200):**
```json
{
  "studentId": "20001",
  "studentName": "Alice Johnson",
  "currentSemester": {
    "semesterId": 2,
    "semesterName": "Spring",
    "academicYear": "2024-2025",
    "gpa": 0.0,
    "cgpa": 3.4,
    "registeredHours": 12,
    "earnedHours": 0,
    "enrollments": [
      {
        "courseCode": "CS201",
        "courseName": "Data Structures",
        "credits": 3,
        "letterGrade": null,
        "coursework": 40,
        "exam": null,
        "hasGrade": false,
        "isInProgress": true
      }
    ],
    "completedCourses": 0,
    "inProgressCourses": 4
  }
}
```

---

### GET /student/available-registrations/
Get courses available for registration with prerequisite validation.

**Response (200):**
```json
{
  "studentId": "20001",
  "studentName": "Alice Johnson",
  "accessibleDepartments": ["CS", "GP"],
  "registrationsByLevel": {
    "1": [
      {
        "registrationId": 123,
        "courseCode": "CS101",
        "courseName": "Introduction to Programming",
        "credits": 3,
        "level": 1,
        "groupNumber": 1,
        "capacity": 30,
        "isEnrolled": false,
        "schedulePatterns": [
          {
            "patternId": 456,
            "patternName": "Main Lecture",
            "patternType": "LEC",
            "capacity": 30,
            "timeSlots": [
              {
                "day": 1,
                "dayName": "Sunday",
                "startPeriod": 1,
                "endPeriod": 2,
                "location": "A101",
                "educator": {
                  "id": "12345",
                  "name": "Dr. Smith"
                }
              }
            ]
          }
        ]
      }
    ]
  },
  "totalEligibleCourses": 8
}
```

---

### POST /student/register/
Register for courses with pattern selection.

**Request:**
```json
[
  {
    "registrationId": 123,
    "schedulePatterns": [
      {"patternId": 456},
      {"patternId": 789}
    ]
  },
  {
    "registrationId": 124,
    "schedulePatterns": []
  }
]
```

**Response (200):**
```json
{
  "successful": [
    {
      "registrationId": 123,
      "courseCode": "CS101",
      "enrollmentId": 321,
      "action": "created"
    },
    {
      "registrationId": 124,
      "courseCode": "CS102",
      "action": "deleted"
    }
  ],
  "failed": [
    {
      "registration": 125,
      "error": "Pattern 'Tutorial 1' is full (30/30)"
    }
  ]
}
```

**Errors:**
- `400` - Invalid data format
- `403` - Registration period closed
- `404` - Student not found

---

### GET /student/timetable/
Get personal class schedule for current semester.

**Response (200):**
```json
{
  "studentId": "20001",
  "studentName": "Alice Johnson",
  "academicYear": "2024-2025",
  "semester": "fall",
  "timetable": [
    {
      "courseCode": "CS101",
      "patternName": "Main Lecture",
      "start": 1,
      "end": 2,
      "educator": "Dr. Smith",
      "location": "A101"
    },
    {
      "courseCode": "CS101",
      "patternName": "Lab Section A",
      "start": 5,
      "end": 6,
      "educator": "TA Johnson",
      "location": "Lab 1"
    }
  ]
}
```

---

## Educator Endpoints

### GET /educator/info/
Get educator profile information.

**Response (200):**
```json
{
  "educatorId": "12345",
  "nameEn": "Dr. John Smith",
  "nameAr": "د. جون سميث",
  "email": "j.smith@university.edu",
  "phone": "+1234567890",
  "dateOfBirth": "1980-05-15",
  "address": "123 University Ave",
  "degrees": "PhD Computer Science, MIT",
  "department": "Computer Science"
}
```

---

### GET /educator/current-courses/
Get list of courses taught in current semester.

**Response (200):**
```json
{
  "educatorId": "12345",
  "educatorName": "Dr. John Smith",
  "academicYear": "2024-2025",
  "semester": "Fall",
  "courses": [
    {
      "registrationId": 123,
      "courseCode": "CS101",
      "courseName": "Introduction to Programming",
      "credits": 3,
      "groupNumber": 1,
      "enrolledStudents": 25,
      "capacity": 30
    },
    {
      "registrationId": 124,
      "courseCode": "CS201",
      "courseName": "Data Structures",
      "credits": 3,
      "groupNumber": 2,
      "enrolledStudents": 28,
      "capacity": 30
    }
  ]
}
```

---

### GET /educator/course/{registration_id}/
Get detailed course information with student roster and grades.

**Response (200):**
```json
{
  "educatorId": "12345",
  "educatorName": "Dr. John Smith",
  "academicYear": "2024-2025",
  "semester": "Fall",
  "courseInfo": {
    "registrationId": 123,
    "courseCode": "CS101",
    "courseName": "Introduction to Programming",
    "credits": 3,
    "groupNumber": 1,
    "capacity": 30,
    "level": 1,
    "totalEnrolled": 25,
    "studentsWithGrades": 15,
    "studentsWithoutGrades": 10
  },
  "students": [
    {
      "enrollmentId": 456,
      "studentId": "20001",
      "studentName": "Alice Johnson",
      "studentNameAr": "أليس جونسون",
      "level": 2,
      "department": "CS",
      "patterns": [
        {
          "patternName": "Main Lecture",
          "patternType": "LEC"
        },
        {
          "patternName": "Lab Section A",
          "patternType": "LAB"
        }
      ],
      "letterGrade": "A-",
      "numericGrade": 87.5,
      "coursework": 44,
      "courseworkMax": 50,
      "exam": 43,
      "examMax": 50,
      "total": 87,
      "hasGrade": true
    }
  ]
}
```

**Errors:**
- `403` - Not authorized to view this course
- `404` - Registration not found

---

### PUT /educator/course/{registration_id}/grades/
Batch update student grades with automatic GPA calculation.

**Request:**
```json
[
  {
    "enrollmentId": 456,
    "coursework": 45,
    "exam": 42
  },
  {
    "enrollmentId": 789,
    "coursework": 38
  }
]
```

**Response (200):**
```json
{
  "successful": [
    {
      "enrollmentId": 456,
      "studentId": "20001",
      "studentName": "Alice Johnson",
      "coursework": 45,
      "exam": 42,
      "total": 87,
      "letterGrade": "A-",
      "numericGrade": 87.0,
      "semesterGPA": 3.2,
      "cumulativeGPA": 3.4
    }
  ],
  "failed": [
    {
      "enrollmentId": 789,
      "error": "Coursework must be between 0 and 50"
    }
  ],
  "message": "Updated 1 students successfully"
}
```

**Business Rules:**
- Teaching Assistants cannot update exam grades
- Grades must be within valid ranges (0 to max points)
- Semester GPA only calculated when all courses are complete
- CGPA only includes completed semesters

**Errors:**
- `403` - Not authorized / TA trying to update exam grades
- `404` - Registration or enrollment not found

---

### GET /educator/timetable/
Get teaching schedule for current semester.

**Response (200):**
```json
{
  "educatorId": "12345",
  "educatorName": "Dr. John Smith",
  "academicYear": "2024-2025",
  "semester": "Fall",
  "timetable": [
    {
      "courseCode": "CS101",
      "courseName": "Introduction to Programming",
      "patternName": "Main Lecture",
      "patternType": "LEC",
      "day": "Sunday",
      "start": 1,
      "end": 2,
      "location": "A101",
      "groupNumber": 1
    }
  ]
}
```

---

## Admin Endpoints

### GET /settings/
Get global system settings.

**Response (200):**
```json
{
  "current_academic_year": "2024-2025",
  "current_semester": "fall",
  "registration_open": true
}
```

### PUT /settings/
Update global system settings.

**Request:**
```json
{
  "current_academic_year": "2024-2025",
  "current_semester": "spring",
  "registration_open": false
}
```

**Permissions:** Admin only

---

### CRUD Operations

All major entities support full CRUD operations with admin permissions:

- **Students**: `GET|POST /students/`, `GET|PUT|DELETE /student/{id}/`
- **Courses**: `GET|POST /courses/`, `GET|PUT|DELETE /course/{id}/`
- **Educators**: `GET|POST /educators/`, `GET|PUT|DELETE /educator/{id}/`
- **Departments**: `GET|POST /departments/`, `GET|PUT|DELETE /department/{id}/`
- **Registrations**: `GET|POST /registrations/`, `GET|PUT|DELETE /registration/{id}/`
- **Enrollments**: `GET|POST /enrollments/`, `GET|PUT|DELETE /enrollment/{id}/`

---

## Error Responses

### Standard Error Format
```json
{
  "error": "Description of what went wrong",
  "detail": "Additional context (optional)"
}
```

### Common Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request (invalid data)
- **401** - Unauthorized (no/invalid token)
- **403** - Forbidden (insufficient permissions)
- **404** - Not Found
- **500** - Internal Server Error

---

## Rate Limiting

API requests are rate-limited per user:
- **Authenticated users**: Higher limits
- **Anonymous users**: Lower limits

Rate limit headers included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
```
