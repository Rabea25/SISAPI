from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator, MaxLengthValidator

class Student(models.Model):
    nameAr = models.CharField(max_length=200, blank=False)
    nameEn = models.CharField(max_length=200, blank=False)
    studentId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    level = models.SmallIntegerField(default=0, blank=True, null=False, validators=[MaxValueValidator(4)])
    earnedHours = models.SmallIntegerField(default=0, blank=True, null=False)
    statusChoices = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
    ]
    nationalId = models.CharField(max_length=14, unique=True, blank=False, null=False, validators=[MinLengthValidator(14), MaxLengthValidator(14)])
    status = models.CharField(choices=statusChoices, max_length=10, default='active', blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    dateOfBirth = models.DateField(blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return f"{self.nameAr} / {self.nameEn} "

class Course(models.Model):
    courseName = models.CharField(max_length=200, blank=False, null=False)
    courseCode = models.CharField(max_length=6, unique=True, blank=False, null=False, primary_key=True)
    credits = models.SmallIntegerField(default=3, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    level = models.SmallIntegerField(default=0, blank=True, null=False)
    typeChoices = [
        ('core', 'Core'),
        ('specialization', 'Specialization'),
    ]
    type = models.CharField(choices=typeChoices, max_length=15, default='core', blank=True, null=False)

    def __str__(self):
        return f"{self.courseName} ({self.courseCode})"

class AcademicYear(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="academic_years")
    yearName = models.CharField(max_length=10)
    yearId = models.AutoField(primary_key=True)
    def __str__(self):
        return f"{self.student.nameEn} - {self.yearName}"

class Semester(models.Model):
    semesterId = models.AutoField(primary_key=True)
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

    def __str__(self):
        return f"{self.academicYear} - {self.get_semesterName_display()}"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=3, unique=True, blank=False, null=False, primary_key=True)

    def __str__(self):
        return self.name


class Educator(models.Model):
    nameAr = models.CharField(max_length=200)
    nameEn = models.CharField(max_length=200)
    nationalId = models.CharField(max_length=14, unique=True, blank=False, null=False)
    educatorId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    type_choices = [
        ('Teaching Assistant', 'Teaching Assistant'),
        ('Lecturer', 'Lecturer'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
    ]
    type = models.CharField(max_length=30, choices=type_choices, blank=False, null=False, default='Lecturer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='educators', blank=True, null=True)

    def __str__(self):
        return f"{self.nameAr} / {self.nameEn}"

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

    def __str__(self):
        return f"{self.student.nameEn} - {self.course.courseCode} ({self.semester.semesterName})"


class TimeSlot(models.Model):
    """
    Represents a single, recurring session for an enrolled course.
    e.g., a lecture, lab, or tutorial.
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='timeslots')
    
    SESSION_TYPE_CHOICES = [
        ('LEC', 'Lecture'),
        ('LAB', 'Lab'),
        ('TUT', 'Tutorial'),
    ]
    sessionType = models.CharField(max_length=3, choices=SESSION_TYPE_CHOICES, default='LEC')

    DAY_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
    ]
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)

    startTime = models.TimeField()
    endTime = models.TimeField()
    
    location = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 'Room 301' or 'Online'")

    class Meta:
        ordering = ['day', 'startTime']
        unique_together = [['enrollment', 'day', 'startTime']]

    def __str__(self):
        return f"{self.enrollment.course.courseCode} {self.get_sessionType_display()} on {self.get_day_display()} at {self.startTime}"
