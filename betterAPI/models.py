from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator

class GlobalSettings(models.Model):
    """
    Simple singleton model to track current academic year and semester
    """
    current_academic_year = models.CharField(max_length=10, help_text="e.g., '2024-2025'")
    current_semester = models.CharField(
        max_length=10,
        choices=[('fall', 'Fall'), ('spring', 'Spring'), ('summer', 'Summer')],
        default='fall'
    )
    registration_open = models.BooleanField(default=False, help_text="Is registration currently open?")

    class Meta:
        verbose_name = "Global Settings"
        verbose_name_plural = "Global Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and GlobalSettings.objects.exists():
            raise ValidationError("Only one GlobalSettings instance allowed")
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        """Get the current global settings (create if doesn't exist)"""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'current_academic_year': '2024-2025',
                'current_semester': 'fall'
            }
        )
        return obj

    def __str__(self):
        return f"AY {self.current_academic_year} - {self.get_current_semester_display()}"

class Student(models.Model):
    nameAr = models.CharField(max_length=200, blank=False)
    nameEn = models.CharField(max_length=200, blank=False)
    Gender = models.CharField(choices=[('male' , 'male'), ('female' , 'female')], blank=True, null=True)
    nationality =  models.CharField(max_length=50, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    homePhone = models.CharField(max_length=15, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
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
    
    def calculate_gpa(self, student):
        """Calculate semester GPA for a specific student"""
        enrollments = self.enrollments.filter(
            student=student,
            letterGrade__isnull=False
        ).exclude(letterGrade='')
        
        if not enrollments:
            return 0.0
            
        total_points = 0
        total_credits = 0
        
        for enrollment in enrollments:
            grade_points = self.get_grade_points(enrollment.letterGrade)
            if grade_points is None:  # Invalid grade
                continue
                
            credits = enrollment.registration.course.credits
            total_points += grade_points * credits
            total_credits += credits
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    
    def calculate_cgpa(self, student):
        """Calculate cumulative GPA across all semesters for a student"""
        # Get all previous semesters for this student with non-zero GPA
        all_semesters = Semester.objects.filter(
            academicYear__student=student,
            gpa__gt=0
        ).order_by('academicYear__yearName', 'semesterName')
        
        if not all_semesters:
            return 0.0
            
        total_points = 0
        total_credits = 0
        
        for semester in all_semesters:
            semester_enrollments = semester.enrollments.filter(
                student=student,
                letterGrade__isnull=False
            ).exclude(letterGrade='')
            
            for enrollment in semester_enrollments:
                grade_points = self.get_grade_points(enrollment.letterGrade)
                if grade_points is not None:
                    credits = enrollment.registration.course.credits
                    total_points += grade_points * credits
                    total_credits += credits
        
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    
    @staticmethod
    def get_grade_points(letter_grade):
        """Convert letter grade to points (4.0 scale)"""
        grade_map = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }
        return grade_map.get(letter_grade)
    
    def is_complete_semester(self, student):
        """Check if all courses in semester have grades assigned"""
        enrollments = self.enrollments.filter(student=student)
        return all(
            enrollment.letterGrade and enrollment.letterGrade.strip()
            for enrollment in enrollments
        )

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=3, unique=True, blank=False, null=False, primary_key=True)

    def __str__(self):
        return self.name


class Educator(models.Model):
    nameAr = models.CharField(max_length=200)
    nameEn = models.CharField(max_length=200)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    nationalId = models.CharField(max_length=14, unique=True, blank=False, null=False)
    educatorId = models.CharField(max_length=5, unique=True, blank=False, null=False, primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    homePhone = models.CharField(max_length=15, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    degrees = models.TextField(blank=True, default=" ", null=True)
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
    A course offering. Students can register for this.
    No semester dependency - uses GlobalSettings for current semester.
    Level comes from the Course itself.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    group_number = models.PositiveIntegerField(help_text="Group number for this course (1, 2, 3, etc.)")
    capacity = models.PositiveIntegerField(default=60, help_text="Total capacity for this course group")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [['course', 'group_number']]

    def __str__(self):
        return f"{self.course.courseCode} - Group {self.group_number}"

    @property
    def level(self):
        """Get level from the course"""
        return self.course.level

class SchedulePattern(models.Model):
    """
    A selectable component within a registration (like "Tutorial 1", "Lab A", "Main Lecture").
    Students select one or more patterns when enrolling.
    Pattern capacity should be <= Registration capacity.
    """
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='patterns')
    pattern_name = models.CharField(max_length=100, help_text="e.g., 'Tutorial 1', 'Lab Section A', 'Main Lecture'")
    pattern_type = models.CharField(
        max_length=3,
        choices=[('LEC', 'Lecture'), ('LAB', 'Lab'), ('TUT', 'Tutorial')],
        default='LEC'
    )
    capacity = models.PositiveIntegerField(default=30, help_text="Capacity for this specific section (should be <= registration capacity)")

    
    class Meta:
        unique_together = [['registration', 'pattern_name']]

    def __str__(self):
        return f"{self.registration.course.courseCode} - {self.pattern_name}"

    def clean(self):
        """Validate that pattern capacity doesn't exceed registration capacity"""
        if self.capacity and self.registration_id:
            if self.capacity > self.registration.capacity:
                raise ValidationError(f"Pattern capacity ({self.capacity}) cannot exceed registration capacity ({self.registration.capacity})")

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
    
    def calculate_total_and_grade(self):
        """Calculate total score and assign letter grade"""
        if self.coursework is None or self.exam is None:
            return
            
        self.total = (self.coursework or 0) + (self.exam or 0)
        
        # Calculate percentage
        max_total = (self.courseworkMax or 50) + (self.examMax or 50)
        percentage = (self.total / max_total) * 100 if max_total > 0 else 0
        
        # Assign letter grade based on percentage
        if percentage >= 95:
            self.letterGrade = 'A+'
        elif percentage >= 90:
            self.letterGrade = 'A'
        elif percentage >= 85:
            self.letterGrade = 'A-'
        elif percentage >= 80:
            self.letterGrade = 'B+'
        elif percentage >= 75:
            self.letterGrade = 'B'
        elif percentage >= 70:
            self.letterGrade = 'B-'
        elif percentage >= 65:
            self.letterGrade = 'C+'
        elif percentage >= 60:
            self.letterGrade = 'C'
        elif percentage >= 55:
            self.letterGrade = 'C-'
        elif percentage >= 50:
            self.letterGrade = 'D+'
        elif percentage >= 45:
            self.letterGrade = 'D'
        elif percentage >= 40:
            self.letterGrade = 'D-'
        else:
            self.letterGrade = 'F'
            
        # Calculate numeric grade (percentage)
        self.numericGrade = round(percentage, 2)
    
    def get_all_time_slots(self):
        """Returns all time slots for this enrollment's selected patterns."""
        return TimeSlot.objects.filter(pattern__in=self.selected_patterns.all())

    def clean(self):
        """
        Validates that the student has selected exactly one pattern of each type
        that exists for this registration.
        """
        if not self.pk:
            # Skip validation for new instances before they're saved
            return
            
        # Get all pattern types available for this registration
        available_types = self.registration.patterns.values_list('pattern_type', flat=True).distinct()
        selected_patterns = self.selected_patterns.all()
        
        # Check each pattern type
        for pattern_type in available_types:
            patterns_of_type = selected_patterns.filter(pattern_type=pattern_type)
            count = patterns_of_type.count()
            
            if count == 0:
                raise ValidationError(f"You must select exactly one {pattern_type} pattern.")
            elif count > 1:
                raise ValidationError(f"You can only select one {pattern_type} pattern, but {count} were selected.")
    
    def save(self, *args, **kwargs):
        # Save the instance first
        super().save(*args, **kwargs)
        
        # Only validate pattern selection if patterns have been set
        if self.selected_patterns.exists():
            self.clean()

    def is_complete_enrollment(self):
        """
        Returns True if the student has selected exactly one pattern of each 
        required type for this registration.
        """
        try:
            self.clean()
            return True
        except ValidationError:
            return False
    
    def get_missing_pattern_types(self):
        """
        Returns a list of pattern types that the student still needs to select.
        """
        available_types = self.registration.patterns.values_list('pattern_type', flat=True).distinct()
        selected_types = self.selected_patterns.values_list('pattern_type', flat=True).distinct()
        
        missing_types = []
        for pattern_type in available_types:
            selected_count = self.selected_patterns.filter(pattern_type=pattern_type).count()
            if selected_count == 0:
                missing_types.append(pattern_type)
        
        return missing_types
    



    