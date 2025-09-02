from rest_framework import serializers
from . models import Student, Course, AcademicYear, Semester, Department, Educator, Registration, Enrollment, SchedulePattern, TimeSlot, GlobalSettings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, data):
        if not data.get('nameEn') or not data.get('nameAr'):
            raise ValidationError("Both English and Arabic names are required.")
        return data

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'
    

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EducatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Educator
        fields = '__all__'

    def validate(self, data):
        if not data.get('nameEn') or not data.get('nameAr'):
            raise ValidationError("Both English and Arabic names are required.")
        return data

class UserCreationSerializer(serializers.Serializer):
    """
    Serializer for creating a User from a Student or Educator.
    Validates that the source object exists and a user doesn't already.
    """
    id = serializers.CharField(max_length=10)
    type = serializers.ChoiceField(choices=['student', 'educator'])

    def validate(self, data):
        user_id = data.get('id')
        user_type = data.get('type')
        source_model = Student if user_type == 'student' else Educator

        try:
            # Check if the student or educator exists
            instance = source_model.objects.get(pk=user_id)
            data['source_object'] = instance
        except source_model.DoesNotExist:
            raise serializers.ValidationError(f"No {user_type} found with the ID '{user_id}'.")
        
        # Check if a user account already exists for this ID
        if User.objects.filter(username=user_id).exists():
            raise serializers.ValidationError(f"A user with the username '{user_id}' already exists.")

        return data


class GlobalSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for GlobalSettings model - current academic year and semester
    """
    current_semester_display = serializers.CharField(source='get_current_semester_display', read_only=True)
    
    class Meta:
        model = GlobalSettings
        fields = ['id', 'current_academic_year', 'current_semester', 'current_semester_display', 'registration_open']

    def validate(self, data):
        # Ensure only one GlobalSettings instance
        if self.instance is None and GlobalSettings.objects.exists():
            raise ValidationError("GlobalSettings instance already exists. Use PUT to update.")
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Registration model - course offerings (no semester dependency)
    Level comes from the course automatically.
    """
    course_name = serializers.CharField(source='course.courseName', read_only=True)
    course_code = serializers.CharField(source='course.courseCode', read_only=True)
    level = serializers.IntegerField(source='course.level', read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'course', 'course_code', 'course_name', 'level', 'group_number', 'capacity', 'is_active']

    def validate(self, data):
        course = data.get('course')
        group_number = data.get('group_number')
        
        # Check for unique registration (without level since it comes from course)
        if Registration.objects.filter(
            course=course, group_number=group_number
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(
                f"Registration for {course.courseCode} Group {group_number} already exists."
            )
        return data


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Enrollment model - student registrations with grades
    """
    student_name = serializers.CharField(source='student.nameEn', read_only=True)
    student_id = serializers.CharField(source='student.studentId', read_only=True)
    course_code = serializers.CharField(source='registration.course.courseCode', read_only=True)
    course_name = serializers.CharField(source='registration.course.courseName', read_only=True)
    semester_name = serializers.CharField(source='semester.get_semesterName_display', read_only=True)
    academic_year = serializers.CharField(source='semester.academicYear.yearName', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_id', 'student_name', 'registration', 
                 'course_code', 'course_name', 'semester', 'semester_name', 'academic_year',
                 'selected_patterns', 'letterGrade', 'numericGrade', 'courseworkMax', 
                 'coursework', 'examMax', 'exam', 'total']

    def validate(self, data):
        student = data.get('student')
        registration = data.get('registration')
        
        # Check for unique enrollment
        if Enrollment.objects.filter(
            student=student, registration=registration
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(
                f"Student {student.studentId} is already enrolled in {registration.course.courseCode}."
            )
        
        # Validate semester consistency
        if data.get('semester') != registration.semester:
            raise ValidationError("Enrollment semester must match registration semester.")
            
        return data


class SchedulePatternSerializer(serializers.ModelSerializer):
    """
    Serializer for SchedulePattern model - lecture/lab/tutorial sections
    """
    registration_info = serializers.CharField(source='registration.__str__', read_only=True)
    
    class Meta:
        model = SchedulePattern
        fields = ['id', 'registration', 'registration_info', 'pattern_name', 'pattern_type', 'capacity']

    def validate(self, data):
        registration = data.get('registration')
        pattern_name = data.get('pattern_name')
        
        # Check for unique pattern name within registration
        if SchedulePattern.objects.filter(
            registration=registration, pattern_name=pattern_name
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError(
                f"Pattern '{pattern_name}' already exists for this registration."
            )
        return data


class TimeSlotSerializer(serializers.ModelSerializer):
    """
    Serializer for TimeSlot model - specific class times
    """
    pattern_info = serializers.CharField(source='pattern.__str__', read_only=True)
    educator_name = serializers.CharField(source='educator.nameEn', read_only=True)
    day_name = serializers.CharField(source='get_day_display', read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'pattern', 'pattern_info', 'day', 'day_name', 'start_period', 
                 'end_period', 'location', 'educator', 'educator_name']

