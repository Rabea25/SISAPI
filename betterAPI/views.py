from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Student, Course, AcademicYear, Semester, Department, Educator
from . import serializers
from django.shortcuts import get_object_or_404, render
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsManager
from django.contrib.auth.models import User, Group

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

class UserCreateView(generics.CreateAPIView):

    serializer_class = serializers.UserCreationSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        user_id = validated_data.get('id')
        user_type = validated_data.get('type')
        source_object = validated_data.get('source_object')

        # Create the user with the national ID as the password
        user = User.objects.create_user(
            username=user_id,
            password=source_object.nationalId
        )

        # Assign the user to the appropriate group
        group = Group.objects.get(name=f"{user_type.capitalize()}")
        user.groups.add(group)
    

        return Response(
            {"message": f"Successfully created user for {user_type} '{user_id}'."},
            status=status.HTTP_201_CREATED
        )

