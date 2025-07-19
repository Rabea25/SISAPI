from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator

class Student(models.Model):
    nameAr = models.CharField(max_length=200, blank=False)
    nameEn = models.CharField(max_length=200, blank=False)
    studentId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    level = models.SmallIntegerField(default=0, blank=True, null=False, validators=[MaxValueValidator(4)])
    earnedHours = models.SmallIntegerField(default=0, blank=True, null=False)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='students')
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
    departments = models.ManyToManyField('Department', related_name='courses', help_text="Departments that can access this course")
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

class Registration(models.Model):
    """
    A course offering in a semester. Students can register for this.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='registrations')
    level = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    group_number = models.PositiveIntegerField(help_text="Group within the level (1, 2, 3, etc.)")
    capacity = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['course', 'semester', 'level', 'group_number']]

    def __str__(self):
        return f"{self.course.courseCode} - Level {self.level} Group {self.group_number} ({self.semester})"

class SchedulePattern(models.Model):
    """
    A selectable component within a registration (like "Tutorial 1", "Lab A", "Main Lecture").
    Students select one or more patterns when enrolling.
    """
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='patterns')
    pattern_name = models.CharField(max_length=100, help_text="e.g., 'Tutorial 1', 'Lab Section A', 'Main Lecture'")
    pattern_type = models.CharField(
        max_length=3,
        choices=[('LEC', 'Lecture'), ('LAB', 'Lab'), ('TUT', 'Tutorial')],
        default='LEC'
    )
    capacity = models.PositiveIntegerField(default=30)

    
    class Meta:
        unique_together = [['registration', 'pattern_name']]

    def __str__(self):
        return f"{self.registration.course.courseCode} - {self.pattern_name}"

class TimeSlot(models.Model):
    """
    A specific time period for a schedule pattern.
    A pattern can have multiple time slots (e.g., a lecture on Sun + Tue).
    """
    pattern = models.ForeignKey(SchedulePattern, on_delete=models.CASCADE, related_name='time_slots')
    educator = models.ForeignKey(Educator, on_delete=models.CASCADE, related_name='time_slots', blank=True, null=True)
    
    DAY_CHOICES = [
        (0, 'Saturday'), (1, 'Sunday'), (2, 'Monday'),
        (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'),
    ]
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_period = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    end_period = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['day', 'start_period']
        unique_together = [['pattern', 'day', 'start_period']]

    def __str__(self):
        return f"{self.pattern.pattern_name} - {self.get_day_display()} P{self.start_period}-{self.end_period}"

    def clean(self):
        if self.start_period and self.end_period and self.end_period < self.start_period:
            raise ValidationError("End period cannot be earlier than start period.")

class Enrollment(models.Model):
    """
    A student's enrollment in a specific registration.
    The selected_patterns field contains the student's choices.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')
    selected_patterns = models.ManyToManyField(SchedulePattern, related_name='enrollments')
    
    # Grade fields
    letterGrade = models.CharField(max_length=2, blank=True, null=True)
    numericGrade = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, blank=True, null=True)
    courseworkMax = models.SmallIntegerField(default=50, blank=True, null=True)
    coursework = models.SmallIntegerField(default=0, blank=True, null=True)
    examMax = models.SmallIntegerField(default=50, blank=True, null=True)
    exam = models.SmallIntegerField(default=0, blank=True, null=True)
    total = models.SmallIntegerField(default=0, blank=True, null=True)

    class Meta:
        unique_together = [['student', 'registration']]

    def __str__(self):
        return f"{self.student.nameEn} - {self.registration.course.courseCode}"
    
    def get_all_time_slots(self):
        """Returns all time slots for this enrollment's selected patterns."""
        return TimeSlot.objects.filter(pattern__in=self.selected_patterns.all())



    