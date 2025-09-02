from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Student, Course, AcademicYear, Semester, Department, Educator, Registration, Enrollment, SchedulePattern, TimeSlot, GlobalSettings
from . import serializers
from django.shortcuts import get_object_or_404, render
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsEducator, IsStudent
from django.contrib.auth.models import User, Group
from django.db.models import Q, Sum
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

# GLOBAL SETTINGS VIEWS
class GlobalSettingsView(generics.RetrieveUpdateAPIView):
    """
    Get or update global settings (current academic year and semester)
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = serializers.GlobalSettingsSerializer
    permission_classes = [IsAdminUser]
    
    def get_object(self):
        # Always return the singleton instance
        return GlobalSettings.get_current()

class GlobalSettingsPublicView(generics.RetrieveAPIView):
    """
    Public view to get current academic year and semester (no auth required)
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = serializers.GlobalSettingsSerializer
    permission_classes = []  # No authentication required
    
    def get_object(self):
        return GlobalSettings.get_current()

class RegistrationListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Registration.objects.all()
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Optimize queries with related data"""
        return Registration.objects.select_related(
            'course'
        ).prefetch_related('patterns')

class RegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Registration.objects.all()
    serializer_class = serializers.RegistrationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Registration.objects.select_related(
            'course'
        ).prefetch_related('patterns')

# ENROLLMENT CRUD VIEWS
class EnrollmentListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Optimize queries with related data"""
        return Enrollment.objects.select_related(
            'student', 'registration__course', 'semester__academicYear'
        ).prefetch_related('selected_patterns')

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Enrollment.objects.all()
    serializer_class = serializers.EnrollmentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Enrollment.objects.select_related(
            'student', 'registration__course', 'semester__academicYear'
        ).prefetch_related('selected_patterns')

# SCHEDULE PATTERN CRUD VIEWS
class SchedulePatternListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = SchedulePattern.objects.all()
    serializer_class = serializers.SchedulePatternSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Optimize queries with related data"""
        return SchedulePattern.objects.select_related(
            'registration__course'
        ).prefetch_related('time_slots')

class SchedulePatternDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = SchedulePattern.objects.all()
    serializer_class = serializers.SchedulePatternSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return SchedulePattern.objects.select_related(
            'registration__course'
        ).prefetch_related('time_slots')

class TimeSlotListCreateView(generics.ListCreateAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = TimeSlot.objects.all()
    serializer_class = serializers.TimeSlotSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Optimize queries with related data"""
        return TimeSlot.objects.select_related(
            'pattern__registration__course', 'educator'
        )

class TimeSlotDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = TimeSlot.objects.all()
    serializer_class = serializers.TimeSlotSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return TimeSlot.objects.select_related(
            'pattern__registration__course', 'educator'
        )

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

class GetCurrentUser(generics.RetrieveAPIView):
    throttle_classe = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(
                {'message': 'User is not authenticated'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if request.user.groups.filter(name='Student'):
            student = Student.objects.get(studentId=request.user.username)
            return Response(
                {"message": "Token is authenticated.", 'id' : student.studentId, 'name' : student.nameEn},
                status=status.HTTP_200_OK
            )
        elif request.user.groups.filter(name='Educator'):
            educator = Educator.objects.get(educatorId=request.user.username)
            return Response(
                {"message": "Token is authenticated.", 'id' : student.studentId, 'name' : student.nameEn},
                status=status.HTTP_200_OK
            )
        elif request.user.is_staff:
            return Response(
                {"message": "Token is authenticated."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message' : 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class StudentInfo(generics.GenericAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        studentId = request.user.username 
        try:
            student = Student.objects.select_related('department').get(studentId=studentId)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        passed_enrollments = student.enrollments.filter( Q(letterGrade__in=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D'])).select_related('registration__course')

        total_credits = passed_enrollments.aggregate(Sum('registration__course__credits'))['registration__course__credits__sum'] or 0
        current_enrollment = student.enrollments.select_related(
            'semester__academicYear'
        ).order_by('-semester__academicYear__yearName', '-semester__semesterName').first()
        
        current_semester = None
        current_academic_year = None
        current_cgpa = 0.0
        if current_enrollment:
            current_semester = current_enrollment.semester.get_semesterName_display()
            current_academic_year = current_enrollment.semester.academicYear.yearName
            current_cgpa = float(current_enrollment.semester.cgpa) if current_enrollment.semester.cgpa else 0.0
        
        # 🎯 STEP 5: Build the response data
        data = {
            # Basic student info
            'studentId': student.studentId,
            'nameAr': student.nameAr,
            'nameEn': student.nameEn,
            'email': student.email,
            'phone': student.phone,
            'dateOfBirth': student.dateOfBirth,
            'address': student.address,
            'gender': student.Gender,
            'nationality': student.nationality,
            'religion': student.religion,
            'homePhone': student.homePhone,
            'zipcode': student.zipcode,
            'nationalId': student.nationalId,
            'status': student.get_status_display(),
            
            # Academic info
            'level': student.level,
            'earnedHours': student.earnedHours,
            'passedCreditHours': total_credits,
            'cgpa': current_cgpa,
            
            # Department info (from related table)
            'department': {
                'code': student.department.code,
                'name': student.department.name,
                'description': student.department.desc
            },
            
            # Current semester info
            'currentSemester': current_semester,
            'currentAcademicYear': current_academic_year,
        }
        
        return Response(data, status=status.HTTP_200_OK)

class StudentGrades(generics.GenericAPIView):
    """
    Returns all academic history: Academic Years -> Semesters -> Enrollments with grades
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        studentId = request.user.username
        try:
            student = Student.objects.get(studentId=studentId)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        academic_years = AcademicYear.objects.filter(student=student).prefetch_related(
            'semesters__enrollments__registration__course',
            'semesters__enrollments__registration__course__departments'
        ).order_by('-yearName')

        data = []
        overall_stats = {
            'totalCreditHours': 0,
            'passedCreditHours': 0,
            'overallCGPA': 0.0,
            'totalSemesters': 0
        }

        for academic_year in academic_years:
            year_data = {
                'yearId': academic_year.yearId,
                'yearName': academic_year.yearName,
                'semesters': []
            }

            for semester in academic_year.semesters.all():
                semester_data = {
                    'semesterId': semester.semesterId,
                    'semesterName': semester.get_semesterName_display(),
                    'gpa': float(semester.gpa) if semester.gpa else 0.0,
                    'cgpa': float(semester.cgpa) if semester.cgpa else 0.0,
                    'registeredHours': semester.registeredHours or 0,
                    'earnedHours': semester.earnedHours or 0,
                    'enrollments': []
                }

                enrollments = semester.enrollments.filter(student=student)
                
                for enrollment in enrollments:
                    course = enrollment.registration.course
                    enrollment_data = {
                        'courseCode': course.courseCode,
                        'courseName': course.courseName,
                        'credits': course.credits,
                        'letterGrade': enrollment.letterGrade,
                        'numericGrade': float(enrollment.numericGrade) if enrollment.numericGrade else 0.0,
                        'coursework': enrollment.coursework or 0,
                        'courseworkMax': enrollment.courseworkMax or 50,
                        'exam': enrollment.exam or 0,
                        'examMax': enrollment.examMax or 50,
                        'total': enrollment.total or 0,
                        'isPassed': enrollment.letterGrade in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-'] if enrollment.letterGrade else False
                    }
                    semester_data['enrollments'].append(enrollment_data)

                    overall_stats['totalCreditHours'] += course.credits
                    if enrollment_data['isPassed']:
                        overall_stats['passedCreditHours'] += course.credits

                if semester_data['enrollments']:
                    year_data['semesters'].append(semester_data)
                    overall_stats['totalSemesters'] += 1
                    if semester.cgpa:
                        overall_stats['overallCGPA'] = float(semester.cgpa)

            if year_data['semesters']:
                data.append(year_data)

        response_data = {
            'studentId': student.studentId,
            'studentName': student.nameEn,
            'academicHistory': data,
            'overallStats': overall_stats
        }

        return Response(response_data, status=status.HTTP_200_OK)

class StudentCurrentSemester(generics.GenericAPIView):
    """
    Returns current semester data with possibly incomplete grades
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        studentId = request.user.username
        try:
            student = Student.objects.get(studentId=studentId)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        current_enrollment = student.enrollments.select_related(
            'semester__academicYear',
            'registration__course'
        ).order_by('-semester__academicYear__yearName', '-semester__semesterName').first()

        if not current_enrollment:
            return Response({
                'message': 'No current semester found',
                'currentSemester': None
            }, status=status.HTTP_200_OK)

        current_semester = current_enrollment.semester
        
        current_enrollments = student.enrollments.filter(
            semester=current_semester
        ).select_related('registration__course')

        semester_data = {
            'semesterId': current_semester.semesterId,
            'semesterName': current_semester.get_semesterName_display(),
            'academicYear': current_semester.academicYear.yearName,
            'gpa': float(current_semester.gpa) if current_semester.gpa else 0.0,
            'cgpa': float(current_semester.cgpa) if current_semester.cgpa else 0.0,
            'registeredHours': current_semester.registeredHours or 0,
            'earnedHours': current_semester.earnedHours or 0,
            'enrollments': []
        }

        total_registered_hours = 0
        completed_courses = 0

        for enrollment in current_enrollments:
            course = enrollment.registration.course
            has_grade = enrollment.letterGrade is not None and enrollment.letterGrade != ''
            
            enrollment_data = {
                'courseCode': course.courseCode,
                'courseName': course.courseName,
                'credits': course.credits,
                'letterGrade': enrollment.letterGrade,
                'numericGrade': float(enrollment.numericGrade) if enrollment.numericGrade else 0.0,
                'coursework': enrollment.coursework or 0,
                'courseworkMax': enrollment.courseworkMax or 50,
                'exam': enrollment.exam or 0,
                'examMax': enrollment.examMax or 50,
                'total': enrollment.total or 0,
                'hasGrade': has_grade,
                'isPassed': enrollment.letterGrade in ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-'] if has_grade else None,
                'isInProgress': not has_grade
            }
            semester_data['enrollments'].append(enrollment_data)
            total_registered_hours += course.credits
            if has_grade:
                completed_courses += 1

        semester_data['totalRegisteredHours'] = total_registered_hours
        semester_data['completedCourses'] = completed_courses
        semester_data['inProgressCourses'] = len(current_enrollments) - completed_courses

        response_data = {
            'studentId': student.studentId,
            'studentName': student.nameEn,
            'currentSemester': semester_data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AvailableRegistration(generics.GenericAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        studentId = request.user.username
        try:
            student = Student.objects.select_related('department').get(studentId=studentId)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        completed_courses = student.enrollments.filter(
            letterGrade__in=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
        ).values_list('registration__course', flat=True) 
        
        current_registrations = student.enrollments.filter(
            letterGrade__isnull=True
        ).values_list('registration__course', flat=True) 

        departments = [student.department.code]
        if student.level > 0:
            departments.append('GP')

        base_registrations = Registration.objects.filter(
            is_active=True,
            course__departments__code__in=departments,
        ).exclude(
            course__courseCode__in=completed_courses
        ).select_related(
            'course'
        ).prefetch_related(
            'course__prerequisites',
            'course__departments',
            'patterns__time_slots__educator',
            'patterns__time_slots'
        )

        
        eligible_registrations = []
        for reg in base_registrations:
            course = reg.course
            prerequisites = course.prerequisites.values_list('courseCode', flat=True)
            
            if prerequisites: 
                incomplete = set(prerequisites) - set(completed_courses)
                if not incomplete:  
                    eligible_registrations.append(reg)  
            else:  
                eligible_registrations.append(reg)  

        
        current_registrations_set = set(current_registrations)
        registrations_by_level = {}

        for reg in eligible_registrations:  
            course_code = reg.course.courseCode
            is_enrolled = course_code in current_registrations_set

            
            patterns_data = []
            for pattern in reg.patterns.all():
                time_slots_data = []
                for time_slot in pattern.time_slots.all():
                    time_slot_data = {
                        'day': time_slot.day,
                        'dayName': time_slot.get_day_display(), 
                        'startPeriod': time_slot.start_period,
                        'endPeriod': time_slot.end_period,
                        'location': time_slot.location,
                        'educator': {
                            'id': time_slot.educator.educatorId if time_slot.educator else None,
                            'name': time_slot.educator.nameEn if time_slot.educator else None
                        } if time_slot.educator else None
                    }
                    time_slots_data.append(time_slot_data)
                
                pattern_data = {
                    'patternId': pattern.id,
                    'patternName': pattern.pattern_name,
                    'patternType': pattern.pattern_type,
                    'capacity': pattern.capacity,
                    'timeSlots': time_slots_data
                }
                patterns_data.append(pattern_data)

            
            registration_data = {
                'registrationId': reg.id,
                'courseCode': reg.course.courseCode,
                'courseName': reg.course.courseName,
                'credits': reg.course.credits,
                'level': reg.level,
                'groupNumber': reg.group_number,
                'capacity': reg.capacity,
                'isEnrolled': is_enrolled,
                'schedulePatterns': patterns_data,
            }

            # Group by level
            level = reg.level
            if level not in registrations_by_level:
                registrations_by_level[level] = []
            registrations_by_level[level].append(registration_data)

        
        response_data = {
            'studentId': student.studentId,
            'studentName': student.nameEn,
            'accessibleDepartments': departments,
            'registrationsByLevel': registrations_by_level,
            'totalEligibleCourses': len(eligible_registrations)
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class StudentRegistrationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        StudentId = request.user.username

        try:
            student = Student.objects.get(studentId=StudentId).prefetch_related('')
        except Student.DoesNotExist:
            return Response({'error' : 'student does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if GlobalSettings.get_current().registration_open == False:
            return Response({'error' : 'Registration period is closed'}, status=status.HTTP_403_FORBIDDEN)
        
