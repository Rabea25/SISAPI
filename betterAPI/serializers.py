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
    
