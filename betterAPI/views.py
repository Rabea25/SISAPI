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
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]

class CourseListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]
    
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]

class EducatorListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Educator.objects.all()
    serializer_class = serializers.EducatorSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]
    
class EducatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Educator.objects.all()
    serializer_class = serializers.EducatorSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]
    
class DepartmentListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]
    
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    
    def get_permissions(self):
        permissionClasses = [IsAuthenticated]
        if self.request.method != 'GET':
            permissionClasses.append(IsAdminUser)
        return [permission() for permission in permissionClasses]