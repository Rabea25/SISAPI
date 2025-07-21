# Frontend & API Design Document

## 🎯 Overview
This document outlines the complete frontend page specifications and corresponding API endpoints for the University Student Information System (SIS). The system supports student academic management with features for registration, grade tracking, scheduling, and administrative functions.

---

## 📱 Frontend Pages Specification

### 1. Student Info Page
**Purpose**: Display comprehensive student profile information  
**Access**: Student (own profile), Admin (any student), Educator (assigned students)

**Page Content**:
- Personal Information (Names in Arabic/English, National ID, Date of Birth)
- Academic Status (Student ID, Department, Current Level, Earned Hours)
- Contact Information (Email, Phone, Home Phone, Address, Zip Code)
- Additional Details (Gender, Nationality, Religion, Status)

**User Stories**:
- As a student, I want to view my complete profile information
- As an admin, I want to access any student's profile for verification
- As an educator, I want to view profiles of students in my classes

**Technical Requirements**:
- Read-only display for students
- Edit capabilities for admins
- Profile picture upload support
- Responsive layout for mobile devices

---

### 2. Grades Page
**Purpose**: Display academic performance across semesters  
**Access**: Student (own grades), Admin (any student), Educator (assigned courses)

**Page Content**:
- Semester listing (e.g., "Fall 2023-2024", "Spring 2023-2024")
- Course details per semester:
  - Course name and code
  - Coursework grade (out of courseworkMax)
  - Final exam grade (out of examMax)
  - Total grade and letter grade
- GPA per semester
- Cumulative GPA (CGPA)
- Academic year progression tracking

**User Stories**:
- As a student, I want to see my grades organized by semester
- As a student, I want to track my GPA progression over time
- As an educator, I want to review grades for courses I teach
- As an admin, I want to generate academic transcripts

**Technical Requirements**:
- Sortable by semester, course, or grade
- GPA calculation validation
- Export to PDF functionality
- Grade trend visualization

---

### 3. Registration Page
**Purpose**: Course registration and schedule selection  
**Access**: Student (during registration periods), Admin (always)

**Page Content**:
- Registration status indicator (open/closed for student ID range)
- Available courses filtered by:
  - Student's department
  - Student's level
  - Prerequisites completion
  - Course capacity availability
- For each course:
  - Course information (name, code, credits, description)
  - Available registration groups
  - Schedule pattern selection (lectures, labs, tutorials)
  - Time slots for each pattern
  - Conflict detection with current schedule
- Current enrollment summary
- Credit hour tracking

**User Stories**:
- As a student, I want to register for courses during open registration periods
- As a student, I want to select specific schedule patterns that fit my timetable
- As a student, I want to see conflicts before confirming registration
- As an admin, I want to control registration access by student ID ranges and time periods

**Technical Requirements**:
- Real-time capacity checking
- Schedule conflict detection
- Multi-step enrollment process (course → group → patterns)
- Registration period enforcement
- Prerequisite validation

---

### 4. Exam Schedule Page
**Purpose**: Display examination timetable  
**Access**: Student (enrolled courses), Admin (all schedules), Educator (assigned courses)

**Page Content**:
- Current semester exam schedule
- For each exam:
  - Course name and code
  - Exam type (Midterm, Final)
  - Date and time
  - Location/Hall
  - Duration
  - Seat number (if assigned)
- Calendar view and list view options
- Conflict detection for overlapping exams

**User Stories**:
- As a student, I want to see all my exam dates and locations
- As a student, I want to export my exam schedule
- As an educator, I want to view exam schedules for my courses
- As an admin, I want to manage exam scheduling and room assignments

**Technical Requirements**:
- Calendar integration
- Print-friendly format
- Mobile notifications for upcoming exams
- Room capacity management

---

### 5. Student ID Display Page
**Purpose**: Digital student ID card  
**Access**: Student (own ID), Admin (any student ID)

**Page Content**:
- Student photo
- Full name (Arabic and English)
- Student ID number
- Department and level
- Academic year
- Barcode/QR code for verification
- University logo and branding
- Card validity period

**User Stories**:
- As a student, I want to display my student ID digitally
- As a student, I want to download/print my ID card
- As a staff member, I want to verify student identity using QR codes

**Technical Requirements**:
- High-resolution image support
- QR code generation for verification
- Print optimization
- Offline availability

---

### 6. Absence & Warnings Page
**Purpose**: Academic alerts and attendance tracking  
**Access**: Student (own records), Admin (all students), Academic Advisor (assigned students)

**Page Content**:
- Active warnings and alerts:
  - Academic warnings (low GPA, failed courses)
  - Attendance warnings (excessive absences)
  - Behavioral warnings
  - Financial holds
- Attendance summary by course
- Warning resolution tracking
- Academic advisor contact information

**User Stories**:
- As a student, I want to see any academic warnings or attendance issues
- As a student, I want to track my attendance across courses
- As an academic advisor, I want to issue and manage student warnings
- As an admin, I want to automate warning generation based on academic rules

**Technical Requirements**:
- Automated warning generation
- Email/SMS notification system
- Warning escalation workflows
- Attendance integration with course schedules

---

### 7. Fees & Payment Page
**Purpose**: Financial information and payment processing  
**Access**: Student (own fees), Admin (all students), Finance Office (payment management)

**Page Content**:
- Current semester fees breakdown
- Payment history
- Outstanding balances
- Payment deadlines
- Bank payment voucher generation
- Payment methods and instructions
- Financial holds and restrictions

**User Stories**:
- As a student, I want to see my current fees and payment status
- As a student, I want to generate bank payment vouchers
- As a student, I want to track my payment history
- As a finance officer, I want to manage student payments and generate reports

**Technical Requirements**:
- Secure payment processing
- Bank integration for voucher generation
- Payment receipt generation
- Automated reminder system

---

### 8. Timetable Page
**Purpose**: Personal class schedule display  
**Access**: Student (own schedule), Admin (any student), Educator (own teaching schedule)

**Page Content**:
- Weekly timetable grid (Saturday-Thursday)
- Time periods (1-12) with actual times
- Course information for each slot:
  - Course name and code
  - Session type (Lecture, Lab, Tutorial)
  - Location
  - Educator name
- Empty slots clearly marked
- Conflict indicators
- Export and print options

**User Stories**:
- As a student, I want to see my weekly class schedule
- As a student, I want to identify free time slots
- As an educator, I want to view my teaching schedule
- As an admin, I want to generate classroom utilization reports

**Technical Requirements**:
- Responsive grid layout
- Real-time updates when registration changes
- Conflict highlighting
- Multiple view formats (weekly, daily)
- Integration with calendar applications

---

## 🔌 API Endpoints

### Existing Endpoints

#### Student Management
```
GET    /api/students/                    # List all students [Admin]
POST   /api/students/                    # Create new student [Admin]
GET    /api/students/{id}/               # Get student details [Admin]
PUT    /api/students/{id}/               # Update student [Admin]
DELETE /api/students/{id}/               # Delete student [Admin]
```

#### Course Management
```
GET    /api/courses/                     # List all courses [Admin]
POST   /api/courses/                     # Create new course [Admin]
GET    /api/courses/{code}/              # Get course details [Admin]
PUT    /api/courses/{code}/              # Update course [Admin]
DELETE /api/courses/{code}/              # Delete course [Admin]
```

#### Educator Management
```
GET    /api/educators/                   # List all educators [Admin]
POST   /api/educators/                   # Create new educator [Admin]
GET    /api/educators/{id}/              # Get educator details [Admin]
PUT    /api/educators/{id}/              # Update educator [Admin]
DELETE /api/educators/{id}/              # Delete educator [Admin]
```

#### Department Management
```
GET    /api/departments/                 # List all departments [Admin]
POST   /api/departments/                 # Create new department [Admin]
GET    /api/departments/{code}/          # Get department details [Admin]
PUT    /api/departments/{code}/          # Update department [Admin]
DELETE /api/departments/{code}/          # Delete department [Admin]
```

#### Academic Year Management
```
GET    /api/academic-years/              # List all academic years [Admin]
POST   /api/academic-years/              # Create new academic year [Admin]
GET    /api/academic-years/{id}/         # Get academic year details [Admin]
PUT    /api/academic-years/{id}/         # Update academic year [Admin]
DELETE /api/academic-years/{id}/         # Delete academic year [Admin]
```

#### Semester Management
```
GET    /api/semesters/                   # List all semesters [Admin]
POST   /api/semesters/                   # Create new semester [Admin]
GET    /api/semesters/{id}/              # Get semester details [Admin]
PUT    /api/semesters/{id}/              # Update semester [Admin]
DELETE /api/semesters/{id}/              # Delete semester [Admin]
```

#### User Management
```
POST   /api/users/create/               # Create user account [Admin]
```

### New Endpoints Required

#### Authentication
```
POST   /api/auth/login/                 # Student/Educator login
POST   /api/auth/refresh/               # Refresh JWT token
POST   /api/auth/logout/                # Logout and invalidate token
POST   /api/auth/change-password/       # Change password
```

#### Student Profile
```
GET    /api/students/{id}/profile/      # Get student profile [Student(own), Admin, Educator]
PUT    /api/students/{id}/profile/      # Update student profile [Admin]
```

#### Grades & Academic Records
```
GET    /api/students/{id}/grades/       # Get all grades [Student(own), Admin, Educator]
GET    /api/students/{id}/semesters/{semester_id}/grades/  # Semester grades
GET    /api/students/{id}/transcript/   # Academic transcript [Student(own), Admin]
PUT    /api/enrollments/{id}/grade/     # Update grade [Educator, Admin]
```

#### Registration System
```
GET    /api/registration-status/        # Check if registration is open
GET    /api/students/{id}/available-registrations/  # Available courses for student
POST   /api/students/{id}/enrollments/              # Enroll in course
PUT    /api/students/{id}/enrollments/{enrollment_id}/  # Update enrollment patterns
DELETE /api/students/{id}/enrollments/{enrollment_id}/  # Drop course
GET    /api/registrations/{id}/patterns/             # Get schedule patterns
POST   /api/enrollments/{id}/select-patterns/        # Select schedule patterns
```

#### Schedule & Timetable
```
GET    /api/students/{id}/timetable/                 # Student timetable [Student(own), Admin]
GET    /api/students/{id}/timetable/{semester_id}/   # Semester timetable
GET    /api/educators/{id}/timetable/                # Educator schedule [Educator(own), Admin]
GET    /api/rooms/{room}/schedule/                   # Room utilization [Admin]
```

#### Exam Management
```
GET    /api/students/{id}/exam-schedule/             # Student exam schedule
GET    /api/semesters/{id}/exam-schedule/            # All exams in semester
POST   /api/exams/                                   # Create exam schedule [Admin]
PUT    /api/exams/{id}/                              # Update exam details [Admin]
```

#### Warnings & Notifications
```
GET    /api/students/{id}/warnings/                  # Student warnings
POST   /api/students/{id}/warnings/                  # Issue warning [Advisor, Admin]
PUT    /api/warnings/{id}/resolve/                   # Resolve warning [Advisor, Admin]
GET    /api/students/{id}/attendance/                # Attendance summary
POST   /api/attendance/                              # Record attendance [Educator]
```

#### Financial Management
```
GET    /api/students/{id}/fees/                      # Student fees [Student(own), Admin, Finance]
GET    /api/students/{id}/payment-history/           # Payment history
POST   /api/students/{id}/payment-voucher/           # Generate payment voucher
POST   /api/payments/                                # Record payment [Finance, Admin]
```

#### Student ID
```
GET    /api/students/{id}/id-card/                   # Digital ID card data
GET    /api/students/{id}/qr-code/                   # Generate verification QR code
```

#### Administrative Controls
```
GET    /api/registration-periods/                    # List registration periods [Admin]
POST   /api/registration-periods/                    # Create registration period [Admin]
PUT    /api/registration-periods/{id}/               # Update registration period [Admin]
DELETE /api/registration-periods/{id}/               # Delete registration period [Admin]
```

---

## 🗄️ Additional Database Tables Needed

### Registration Control
```python
class RegistrationPeriod(models.Model):
    """Controls when students can register"""
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    student_id_range_start = models.CharField(max_length=5)
    student_id_range_end = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    registration_type = models.CharField(
        choices=[('initial', 'Initial Registration'), ('add_drop', 'Add/Drop Period')],
        max_length=10
    )
    description = models.TextField(blank=True)
```

### Exam Scheduling
```python
class ExamSchedule(models.Model):
    """Exam dates and locations"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    exam_type = models.CharField(
        choices=[('midterm', 'Midterm'), ('final', 'Final'), ('quiz', 'Quiz')],
        max_length=10
    )
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)
```

### Warnings & Notifications
```python
class StudentWarning(models.Model):
    """Academic and behavioral warnings"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    warning_type = models.CharField(
        choices=[
            ('academic', 'Academic Performance'),
            ('attendance', 'Attendance'),
            ('behavior', 'Behavioral'),
            ('financial', 'Financial Hold')
        ],
        max_length=20
    )
    message = models.TextField()
    severity = models.CharField(
        choices=[('low', 'Advisory'), ('medium', 'Warning'), ('high', 'Critical')],
        max_length=10
    )
    issued_by = models.ForeignKey(Educator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
```

### Attendance Tracking
```python
class AttendanceRecord(models.Model):
    """Individual attendance records"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('excused', 'Excused')],
        max_length=10
    )
    recorded_by = models.ForeignKey(Educator, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['enrollment', 'time_slot', 'date']]
```

### Fee Management
```python
class FeeStructure(models.Model):
    """Semester fee structure by department"""
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    fee_type = models.CharField(
        choices=[('tuition', 'Tuition'), ('lab', 'Lab Fees'), ('registration', 'Registration'), ('other', 'Other')],
        max_length=20
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.CharField(max_length=200)

class StudentPayment(models.Model):
    """Student payment records"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(
        choices=[('bank', 'Bank Transfer'), ('cash', 'Cash'), ('online', 'Online Payment')],
        max_length=10
    )
    voucher_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')],
        max_length=10
    )
    processed_by = models.ForeignKey(Educator, on_delete=models.CASCADE, null=True, blank=True)
```

---

## 🔧 Technical Implementation Notes

### Authentication Flow
1. **Login**: POST `/api/auth/login/` with username/password
2. **Token Response**: JWT access token + refresh token
3. **Authenticated Requests**: Include `Authorization: Bearer <token>` header
4. **Token Refresh**: Use refresh token to get new access token
5. **Logout**: Invalidate tokens on server

### Registration Business Logic
1. **Time-based Control**: Registration only during active periods
2. **ID Range Control**: Students can only register if their ID falls within the allowed range
3. **Prerequisite Validation**: Check completed courses before allowing registration
4. **Capacity Management**: Prevent over-enrollment in courses and patterns
5. **Conflict Detection**: Ensure no schedule overlaps for selected patterns

### Data Validation
- **Pattern Selection**: Enforce exactly one pattern per type (LEC/LAB/TUT)
- **Grade Calculations**: Automatic GPA/CGPA computation
- **Time Constraints**: Validate time periods and prevent conflicts
- **Academic Rules**: Credit hour limits, prerequisite enforcement

### Performance Considerations
- **Caching**: Cache frequently accessed data (course catalogs, schedules)
- **Database Indexing**: Index on student_id, course_code, semester combinations
- **Pagination**: Implement pagination for large data sets
- **Background Tasks**: Use async tasks for email notifications and report generation

---

## 📋 Implementation Roadmap

### Phase 1: Core Functionality (Weeks 1-2)
- Student authentication and profile management
- Basic grade display
- Simple timetable view

### Phase 2: Registration System (Weeks 3-4)
- Registration period management
- Course enrollment with pattern selection
- Schedule conflict detection

### Phase 3: Enhanced Features (Weeks 5-6)
- Exam scheduling
- Attendance tracking
- Warning system

### Phase 4: Administrative Features (Weeks 7-8)
- Fee management
- Advanced reporting
- System administration tools

### Phase 5: Polish & Optimization (Week 9)
- Performance optimization
- Mobile responsiveness
- User experience improvements

---

## 🎨 Frontend Technology Stack Recommendations

### Core Framework
- **React.js** with TypeScript for type safety
- **Next.js** for server-side rendering and routing
- **Material-UI** or **Ant Design** for consistent UI components

### State Management
- **Redux Toolkit** for global state management
- **React Query** for API data fetching and caching

### Additional Libraries
- **Axios** for HTTP requests
- **React Hook Form** for form handling
- **Date-fns** for date manipulation
- **React Calendar** for schedule views
- **Chart.js** for GPA visualization

### Mobile Support
- **Responsive Design** with CSS Grid/Flexbox
- **Progressive Web App (PWA)** capabilities
- **React Native** (future consideration for native mobile app)

This comprehensive design document provides a complete roadmap for building a professional university SIS with modern web technologies and robust API architecture.
