# University SIS API Documentation

## Project Overview
**Project Name:** BetterEEH - University Student Information System API  
**Framework:** Django REST Framework  
**Database:** SQLite (Development)  
**Created:** July 16, 2025  

### Purpose
Building a comprehensive API-first Student Information System to handle:
- Student registration and management
- Subject/Course management
- Grade tracking and reporting
- Timetable scheduling
- Academic records

---

## Project Structure

```
betterEEH/API/
├── db.sqlite3              # SQLite database
├── manage.py               # Django management script
├── Pipfile                 # Python dependencies
├── Pipfile.lock           # Locked dependencies
├── API/                   # Main project directory
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
└── betterAPI/            # Main app directory
    ├── __init__.py
    ├── admin.py          # Django admin configuration
    ├── apps.py           # App configuration
    ├── models.py         # Database models
    ├── views.py          # API views
    ├── urls.py           # App URL patterns
    ├── tests.py          # Unit tests
    └── migrations/       # Database migrations
```

---

## Current Configuration

### Installed Apps
- `django.contrib.admin`
- `django.contrib.auth`
- `django.contrib.contenttypes`
- `django.contrib.sessions`
- `django.contrib.messages`
- `django.contrib.staticfiles`
- `rest_framework`
- `API` (main app)

### Database
- **Engine:** SQLite3
- **Location:** `BASE_DIR / 'db.sqlite3'`

---

## Models Documentation

### Implemented Models

Here are the current models implemented in `betterAPI/models.py`.

#### 1. `Student`
Represents a single student, storing their ID, names, and academic status.

```python
class Student(models.Model):
    nameAr = models.CharField(max_length=200)
    nameEn = models.CharField(max_length=200)
    studentId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    level = models.SmallIntegerField(default=0, blank=True, null=True)
    earnedHours = models.SmallIntegerField(default=0, blank=True, null=True)
    statusChoices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
    ]
    status = models.CharField(choices=statusChoices, max_length=10, default='active', blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
```

#### 2. `Course`
Represents a general course offered by the university.

```python
class Course(models.Model):
    courseName = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=6, unique=True, blank=False, null=False, primary_key=True)
    credits = models.SmallIntegerField(default=3, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    level = models.SmallIntegerField(default=0, blank=True, null=True)
    typeChoices = [
        ('core', 'Core'),
        ('specialization', 'Specialization'),
    ]
    type = models.CharField(choices=typeChoices, max_length=15, default='core', blank=True, null=True)
```

#### 3. `AcademicYear`
Represents an academic year for a specific student.

```python
class AcademicYear(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="academic_years")
    yearName = models.CharField(max_length=10)
```

#### 4. `Semester`
Represents a specific semester within an academic year.

```python
class Semester(models.Model):
    academicYear = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="semesters")
    courses = models.ManyToManyField(Course, blank=True, related_name='semesters')
    semesterNameOptions = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    ]
    semesterName = models.CharField(choices=semesterNameOptions, max_length=10, default='fall', blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, blank=True, null=True)
    registeredHours = models.SmallIntegerField(default=0, blank=True, null=True)
    earnedHours = models.SmallIntegerField(default=0, blank=True, null=True)
```

#### 5. `Department`
Represents an academic department.

```python
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
```

#### 6. `Educator`
Represents an educator or instructor.

```python
class Educator(models.Model):
    nameAr = models.CharField(max_length=200)
    nameEn = models.CharField(max_length=200)
    educatorId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='educators', blank=True, null=True)
```

#### 7. `Enrollment`
Links a student, a course, and an educator for a specific semester, and holds grade information.

```python
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='enrollments', blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments', blank=True, null=True)
    letterGrade = models.CharField(max_length=2, blank=True, null=True)
    numericGrade = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, blank=True, null=True)
    courseworkMax = models.SmallIntegerField(default=50, blank=True, null=True)
    coursework = models.SmallIntegerField(default=0, blank=True, null=True)
    examMax = models.SmallIntegerField(default=50, blank=True, null=True)
    exam = models.SmallIntegerField(default=0, blank=True, null=True)
    total = models.SmallIntegerField(default=0, blank=True, null=True)
```

#### 8. `Timetable`
Stores the schedule for a specific enrollment, including day, time periods, and session type.

```python
class Timetable(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='timetable_sessions')
    DAY_CHOICES = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    
    PERIOD_CHOICES = [
        (1, 'Period 1 (08:00-09:30)'),
        (2, 'Period 2 (09:45-11:15)'),
        (3, 'Period 3 (11:30-13:00)'),
        (4, 'Period 4 (13:15-14:45)'),
        (5, 'Period 5 (15:00-16:30)'),
        (6, 'Period 6 (16:45-18:15)'),
    ]
    startPeriod = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES)
    endPeriod = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES)

    SESSION_TYPE_CHOICES = [
        ('lecture', 'Lecture'),
        ('lab', 'Lab'),
        ('tutorial', 'Tutorial'),
    ]
    sessionType = models.CharField(max_length=10, choices=SESSION_TYPE_CHOICES, default='lecture')
    location = models.CharField(max_length=100, blank=True, null=True)
```

---

## API Endpoints Documentation

### 🚧 Planned Endpoints

#### Student Management
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

#### Subject Management
- `GET /api/subjects/` - List all subjects
- `POST /api/subjects/` - Create new subject
- `GET /api/subjects/{id}/` - Get subject details
- `PUT /api/subjects/{id}/` - Update subject
- `DELETE /api/subjects/{id}/` - Delete subject

#### Enrollment Management
- `GET /api/enrollments/` - List enrollments
- `POST /api/enrollments/` - Enroll student in subject
- `GET /api/students/{id}/enrollments/` - Get student's enrollments
- `PUT /api/enrollments/{id}/grade/` - Update grade

#### Timetable Management
- `GET /api/timetables/` - List all timetables
- `GET /api/students/{id}/timetable/` - Get student's timetable
- `GET /api/subjects/{id}/schedule/` - Get subject schedule

---

## Development Progress

### ✅ Completed
- [x] Django project setup
- [x] Django REST Framework installation
- [x] Basic project structure
- [x] Settings configuration

### 🚧 In Progress
- [ ] Design and implement core models
- [ ] Set up Django admin interface
- [ ] Create API serializers
- [ ] Implement API views and endpoints
- [ ] Add authentication and permissions

### 📋 To Do
- [ ] Data validation and error handling
- [ ] Unit tests for models and APIs
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Frontend integration planning
- [ ] Deployment configuration

---

## Development Notes

### Quick Commands
```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations  
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

### Learning Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Models Reference](https://docs.djangoproject.com/en/5.2/topics/db/models/)

---

## Change Log

| Date | Changes | Notes |
|------|---------|-------|
| 2025-07-16 | Initial project setup | Created Django project with DRF |
| 2025-07-17 | Updated Models Documentation | Synced documentation with current `models.py`. |
| 2025-07-17 | Refactored Models & Added Timetable | Updated models and added a new Timetable model for scheduling. |
| | | Add new entries as you progress |

---

## Notes & Ideas

### Features to Consider
- Grade point average (GPA) calculation
- Academic transcript generation
- Course prerequisites validation
- Attendance tracking
- Fee management
- Academic calendar integration

### Technical Considerations
- Add pagination for large datasets
- Implement proper error handling
- Add logging for debugging
- Consider caching for performance
- Plan for database optimization

---

*Last Updated: July 17, 2025*
