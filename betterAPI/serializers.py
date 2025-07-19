from rest_framework import serializers
from . models import Student, Course, AcademicYear, Semester, Department, Educator
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

