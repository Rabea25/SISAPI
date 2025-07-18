from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Student, Course, AcademicYear, Semester, Department, Educator
from . import serializers
from django.shortcuts import get_object_or_404, render
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsManager

class StudentListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAdminUser]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = [IsAdminUser]

class CourseListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAdminUser]
    
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAdminUser]

class EducatorListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Educator.objects.all()
    serializer_class = serializers.EducatorSerializer
    permission_classes = [IsAdminUser]
    
class EducatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Educator.objects.all()
    serializer_class = serializers.EducatorSerializer
    permission_classes = [IsAdminUser]
    
class DepartmentListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [IsAdminUser]
    
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [IsAdminUser]
    
class AcademicYearListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = AcademicYear.objects.all()
    serializer_class = serializers.AcademicYearSerializer
    permission_classes = [IsAdminUser]
    
class AcademicYearDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = AcademicYear.objects.all()
    serializer_class = serializers.AcademicYearSerializer
    permission_classes = [IsAdminUser]
    
class SemesterListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [IsAdminUser]

class SemesterDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Semester.objects.all()
    serializer_class = serializers.SemesterSerializer
    permission_classes = [IsAdminUser]
    
