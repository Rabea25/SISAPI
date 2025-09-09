# University Student Information System API

REST API for university course registration and academic management.

## Features

- **Course Registration** - Students can register for courses with pattern selection (lectures, labs, tutorials)
- **Prerequisite Validation** - Automatic checking of course requirements and academic standing
- **Real-time Capacity Management** - Prevents over-enrollment with immediate feedback
- **Academic Tracking** - Complete grade management, GPA calculations, and transcripts
- **Multi-role Authentication** - Separate interfaces for students, educators, and administrators
- **Schedule Management** - Dynamic timetable generation with conflict detection

## Database Structure

The system uses a relational database with key entities:

- **Students** → **Academic Years** → **Semesters** → **Enrollments**
- **Courses** with **Prerequisites** and **Department** associations
- **Registrations** containing **Schedule Patterns** (lecture/lab/tutorial sections)
- **Time Slots** with **Educator** assignments and location details
- **Global Settings** for managing current academic year and registration periods

Students select specific patterns when enrolling, creating flexible scheduling while maintaining capacity limits.

## API Endpoints

### Authentication
- `POST /auth/login/` - User login with JWT token
- `POST /auth/refresh/` - Refresh authentication token
- `GET /auth/me/` - Get current user info

### Student Operations
- `GET /student/info/` - Student profile and academic standing
- `GET /student/grades/` - Complete academic transcript
- `GET /student/current-semester/` - Current semester courses and grades
- `GET /student/available-registrations/` - Courses available for registration
- `POST /student/register/` - Register for courses with pattern selection
- `GET /student/timetable/` - Personal class schedule

### Educator Operations
- `GET /educator/info/` - Educator profile information
- `GET /educator/current-courses/` - List of taught courses this semester
- `GET /educator/course/{id}/` - Detailed course info with student roster
- `GET /educator/timetable/` - Teaching schedule

### Admin Operations
- Full CRUD operations for all entities:
  - `/students/`, `/courses/`, `/educators/`, `/departments/`
  - `/registrations/`, `/enrollments/`, `/schedule-patterns/`, `/time-slots/`
- `GET|PUT /settings/` - Global system settings management

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/Rabea25/SISAPI.git
cd SISAPI
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up database
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Usage Example

Register a student for courses:
```json
POST /student/register/
[
  {
    "registrationId": 123,
    "schedulePatterns": [
      {"patternId": 456},  // Main Lecture
      {"patternId": 789}   // Lab Section A
    ]
  }
]
```

---

