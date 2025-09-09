from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from . import views
urlpatterns = [
    
    path('settings/', views.GlobalSettingsView.as_view(), name='global-settings'),
    path('current-semester/', views.GlobalSettingsPublicView.as_view(), name='current-semester-public'),
    
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<str:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('department/<str:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    
    path('academic-years/', views.AcademicYearListCreateView.as_view(), name='academic-year-list-create'),
    path('academic-year/<str:pk>/', views.AcademicYearDetailView.as_view(), name='academic-year-detail'),
    
    path('semesters/', views.SemesterListCreateView.as_view(), name='semester-list-create'),
    path('semester/<str:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    
    path('registrations/', views.RegistrationListCreateView.as_view(), name='registration-list-create'),
    path('registration/<int:pk>/', views.RegistrationDetailView.as_view(), name='registration-detail'),
    
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('enrollment/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    
    path('schedule-patterns/', views.SchedulePatternListCreateView.as_view(), name='schedule-pattern-list-create'),
    path('schedule-pattern/<int:pk>/', views.SchedulePatternDetailView.as_view(), name='schedule-pattern-detail'),
    
    path('time-slots/', views.TimeSlotListCreateView.as_view(), name='timeslot-list-create'),
    path('time-slot/<int:pk>/', views.TimeSlotDetailView.as_view(), name='timeslot-detail'),
    
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
    path('auth/me/', views.GetCurrentUser.as_view(), name='current-user'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('student/info/', views.StudentInfo.as_view(), name='student-info'),
    path('student/grades/', views.StudentGrades.as_view(), name='student-grades'),
    path('student/current-semester/', views.StudentCurrentSemester.as_view(), name='student-current-semester'),
    path('student/available-registrations/', views.AvailableRegistration.as_view(), name='available-registrations'),
    path('student/register/', views.StudentRegistrationView.as_view(), name='student-registration'),
    path('student/timetable/', views.StudentTimetableView.as_view(), name='student-timetable'),
    path('student/<str:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    
    path('educators/', views.EducatorListCreateView.as_view(), name='educator-list-create'),
    path('educator/info/', views.EducatorInfo.as_view(), name='educator-info'),
    path('educator/current-courses/', views.EducatorCoursesView.as_view(), name='educator-current-courses'),
    path('educator/course/<int:registration_id>/', views.EducatorCourseInfo.as_view(), name='educator-course-info'),
    path('educator/timetable/', views.EducatorTimetableView.as_view(), name='educator-timetable'),
    path('educator/<str:pk>/', views.EducatorDetailView.as_view(), name='educator-detail'),
]