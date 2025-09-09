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
            student = Student.objects.select_related('department').get(studentId=StudentId)
        except Student.DoesNotExist:
            return Response({'error' : 'student does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        global_settings = GlobalSettings.get_current()
        if not global_settings.registration_open:
            return Response({'error' : 'Registration period is closed'}, status=status.HTTP_403_FORBIDDEN)
        
        registrations_data = request.data
        if not isinstance(registrations_data, list) or not registrations_data:
            return Response({'error': 'Invalid data format. Expected a non-empty list of registrations.'}, status=status.HTTP_400_BAD_REQUEST)
        
        successful = []
        failed = []

        for reg_data in registrations_data:
            try: 
                result = self.process_registration(student, reg_data, global_settings)
                successful.append(result)
            except Exception as e:
                failed.append({'registration': reg_data.get('registrationId'), 'error': str(e)})

        return Response({
            'successful': successful,
            'failed': failed
        }, status=status.HTTP_200_OK)
    
    def process_registration(self, student, reg_data, global_settings):
        reg_id = reg_data.get('registrationId')
        pattern_data = reg_data.get('schedulePatterns', [])
        pattern_ids = [pattern.get('patternId') for pattern in pattern_data]

        try:
            registration = Registration.objects.get(id=reg_id, is_active=True)
        except Registration.DoesNotExist:
            raise Exception("Registration not found or inactive")
        
        
        

        
        academic_year, created = AcademicYear.objects.get_or_create(student=student, yearName=global_settings.current_academic_year)
        semester, created = Semester.objects.get_or_create(academicYear=academic_year, semesterName=global_settings.current_semester)
        
        if not pattern_ids:
            try:
                enrollment = Enrollment.objects.get(
                    student=student,
                    registration=registration,
                    semester=semester
                )
                enrollment.delete()
                # Update semester registered hours after deletion
                self.update_semester_registered_hours(semester, student)
                return {
                    'registrationId': reg_id,
                    'courseCode': registration.course.courseCode,
                    'action': 'deleted'
                }
            except Enrollment.DoesNotExist:
                return {
                    'registrationId': reg_id,
                    'courseCode': registration.course.courseCode,
                    'action': 'no_change'
                }
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            registration=registration,
            semester=semester 
        )

        patterns = SchedulePattern.objects.filter(id__in=pattern_ids, registration=registration).prefetch_related('enrollments')
        if patterns.count() != len(pattern_ids):
            raise Exception("Some patterns do not belong to this Registration")

        for pattern in patterns: 
            if pattern.enrollments.count() >= pattern.capacity:
                raise Exception(f"Pattern '{pattern.pattern_name}' is full ({pattern.enrollments.count()}/{pattern.capacity})")

        pattern_types = [pattern.pattern_type for pattern in patterns]
        if len(pattern_types) != len(set(pattern_types)):
            raise Exception("Cannot select multiple patterns of the same type (e.g., 2 tutorials)")

        enrollment.selected_patterns.set(patterns)
        enrollment.save()
        
        # Update semester registered hours after enrollment changes
        self.update_semester_registered_hours(semester, student)

        return {
            'registrationId' : reg_id,
            'courseCode' : registration.course.courseCode,
            'enrollmentId' : enrollment.id,
            'action' : 'created' if created else 'updated'
        }
    
    def update_semester_registered_hours(self, semester, student):
        
        from django.db.models import Sum
        
        total_hours = Enrollment.objects.filter(
            student=student,
            semester=semester
        ).aggregate(
            total=Sum('registration__course__credits')
        )['total'] or 0
        
        semester.registeredHours = total_hours
        semester.save(update_fields=['registeredHours'])


class StudentTimetableView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student_id = request.user.username

        try:
            student = Student.objects.get(studentId=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        

        global_settings = GlobalSettings.get_current()
        enrollments = Enrollment.objects.filter(
            student=student,
            semester__academicYear__yearName=global_settings.current_academic_year,
            semester__semesterName=global_settings.current_semester
        ).select_related(
            'registration__course'
        ).prefetch_related(
            'selected_patterns__time_slots',
            'selected_patterns__time_slots__educator'
        )

        timetable = []

        for enrollment in enrollments:
            for pattern in enrollment.selected_patterns.all():
                for time_slot in pattern.time_slots.all():
                    timetable.append({
                        'courseCode': enrollment.registration.course.courseCode,
                        'patternName': pattern.pattern_name,
                        'start': time_slot.start_period,
                        'end': time_slot.end_period,
                        'educator': time_slot.educator.nameEn if time_slot.educator else None,
                        'location': time_slot.location
                    })


        response = {
            'studentId': student.studentId,
            'studentName': student.nameEn,
            'academicYear': global_settings.current_academic_year,
            'semester': global_settings.current_semester,
            'timetable': timetable
        }

        return Response(response, status=status.HTTP_200_OK)


class EducatorInfo(generics.GenericAPIView):

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        educatorId = request.user.username 
        try:
            educator = Educator.objects.select_related('department').get(educatorId=educatorId)
        except Educator.DoesNotExist:
            return Response({'error': 'Educator not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'educatorId': educator.educatorId,
            'nameAr': educator.nameAr,
            'nameEn': educator.nameEn,
            'email': educator.email,
            'phone': educator.phone,
            'dateOfBirth': educator.dateOfBirth,
            'address': educator.address,
            'degrees': educator.degrees,
            'department': educator.department.nameEn if educator.department else ''
            
        }

        return Response(data, status=status.HTTP_200_OK)


class EducatorCoursesView(generics.GenericAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        educatorId = request.user.username 
        try:
            educator = Educator.objects.select_related('department').get(educatorId=educatorId)
        except Educator.DoesNotExist:
            return Response({'error': 'Educator not found'}, status=status.HTTP_404_NOT_FOUND)
        global_settings = GlobalSettings.get_current()
        
        # Get all registrations where this educator teaches in the current semester
        registrations = Registration.objects.filter(
            patterns__time_slots__educator=educator,
            enrollments__semester__academicYear__yearName=global_settings.current_academic_year,
            enrollments__semester__semesterName=global_settings.current_semester
        ).select_related(
            'course'
        ).distinct()
        
        courses_data = []
        for registration in registrations:
            # Count enrolled students for this registration
            student_count = Enrollment.objects.filter(
                registration=registration,
                semester__academicYear__yearName=global_settings.current_academic_year,
                semester__semesterName=global_settings.current_semester,
                selected_patterns__time_slots__educator=educator
            ).distinct().count()
            
            course_data = {
                'registrationId': registration.id,
                'courseCode': registration.course.courseCode,
                'courseName': registration.course.courseName,
                'credits': registration.course.credits,
                'groupNumber': registration.group_number,
                'enrolledStudents': student_count,
                'capacity': registration.capacity
            }
            courses_data.append(course_data)
        
        response_data = {
            'educatorId': educator.educatorId,
            'educatorName': educator.nameEn,
            'academicYear': global_settings.current_academic_year,
            'semester': global_settings.get_current_semester_display(),
            'courses': courses_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class EducatorCourseInfo(generics.GenericAPIView):
    """
    Shows detailed information about a specific course/registration that an educator teaches,
    including all enrolled students and their grades (if any).
    """
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, registration_id, *args, **kwargs):
        educatorId = request.user.username
        
        try:
            educator = Educator.objects.get(educatorId=educatorId)
        except Educator.DoesNotExist:
            return Response({'error': 'Educator not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            registration = Registration.objects.select_related('course').get(id=registration_id)
        except Registration.DoesNotExist:
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verify that this educator actually teaches this registration
        educator_teaches = registration.patterns.filter(
            time_slots__educator=educator
        ).exists()
        
        if not educator_teaches:
            return Response({'error': 'You are not authorized to view this course'}, status=status.HTTP_403_FORBIDDEN)
        
        global_settings = GlobalSettings.get_current()
        
        # Get all enrollments for this registration in current semester
        enrollments = Enrollment.objects.filter(
            registration=registration,
            semester__academicYear__yearName=global_settings.current_academic_year,
            semester__semesterName=global_settings.current_semester
        ).select_related(
            'student'
        ).prefetch_related(
            'selected_patterns__time_slots'
        )
        
        # Filter enrollments to only include students in patterns taught by this educator
        relevant_enrollments = []
        for enrollment in enrollments:
            # Check if student has selected any pattern taught by this educator
            if enrollment.selected_patterns.filter(time_slots__educator=educator).exists():
                relevant_enrollments.append(enrollment)
        
        students_data = []
        for enrollment in relevant_enrollments:
            # Get the patterns this educator teaches for this student
            educator_patterns = enrollment.selected_patterns.filter(
                time_slots__educator=educator
            ).distinct()
            
            patterns_info = []
            for pattern in educator_patterns:
                patterns_info.append({
                    'patternName': pattern.pattern_name,
                    'patternType': pattern.pattern_type
                })
            
            student_data = {
                'enrollmentId': enrollment.id,
                'studentId': enrollment.student.studentId,
                'studentName': enrollment.student.nameEn,
                'studentNameAr': enrollment.student.nameAr,
                'level': enrollment.student.level,
                'department': enrollment.student.department.code,
                'patterns': patterns_info,
                # Grade information
                'letterGrade': enrollment.letterGrade,
                'numericGrade': float(enrollment.numericGrade) if enrollment.numericGrade else None,
                'coursework': enrollment.coursework,
                'courseworkMax': enrollment.courseworkMax,
                'exam': enrollment.exam,
                'examMax': enrollment.examMax,
                'total': enrollment.total,
                'hasGrade': enrollment.letterGrade is not None and enrollment.letterGrade != ''
            }
            students_data.append(student_data)
        
        # Sort students by name
        students_data.sort(key=lambda x: x['studentName'])
        
        course_info = {
            'registrationId': registration.id,
            'courseCode': registration.course.courseCode,
            'courseName': registration.course.courseName,
            'credits': registration.course.credits,
            'groupNumber': registration.group_number,
            'capacity': registration.capacity,
            'level': registration.course.level,
            'totalEnrolled': len(students_data),
            'studentsWithGrades': len([s for s in students_data if s['hasGrade']]),
            'studentsWithoutGrades': len([s for s in students_data if not s['hasGrade']])
        }
        
        response_data = {
            'educatorId': educator.educatorId,
            'educatorName': educator.nameEn,
            'academicYear': global_settings.current_academic_year,
            'semester': global_settings.get_current_semester_display(),
            'courseInfo': course_info,
            'students': students_data
        }
        #TODO: add put method to update grades 
        return Response(response_data, status=status.HTTP_200_OK)

class EducatorTimetableView(generics.GenericAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def get(self, request, registration_id, *args, **kwargs):
        educatorId = request.user.username
        global_settings = GlobalSettings.get_current()

        try:
            educator = Educator.objects.get(educatorId=educatorId)
        except Educator.DoesNotExist:
            return Response({'error': 'Educator not found'}, status=status.HTTP_404_NOT_FOUND)

        time_slots = TimeSlot.objects.filter(
            educator=educator,
            pattern__registration__enrollments__semester__academicYear__yearName=global_settings.current_academic_year,
            pattern__registration__enrollments__semester__semesterName=global_settings.current_semester
        ).select_related(
            'pattern__registration__course'
        ).distinct()

        timetable = []
        for time_slot in time_slots:
            timetable.append({
                'courseCode': time_slot.pattern.registration.course.courseCode,
                'courseName': time_slot.pattern.registration.course.courseName,
                'patternName': time_slot.pattern.pattern_name,
                'patternType': time_slot.pattern.pattern_type,
                'day': time_slot.day,
                'start': time_slot.start_period,
                'end': time_slot.end_period,
                'location': time_slot.location,
                'groupNumber': time_slot.pattern.registration.group_number
            })
        return Response({
            'educatorId': educator.educatorId,
            'educatorName': educator.nameEn,
            'academicYear': global_settings.current_academic_year,
            'semester': global_settings.get_current_semester_display(),
            'timetable': timetable
        }, status=status.HTTP_200_OK)
    
