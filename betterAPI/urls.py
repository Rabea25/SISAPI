from django.urls import path
from .views import EducatorDetailView, EducatorListCreateView, StudentListCreateView, StudentDetailView, CourseListCreateView, CourseDetailView, DepartmentListCreateView, DepartmentDetailView, AcademicYearListCreateView, AcademicYearDetailView, SemesterListCreateView, SemesterDetailView
urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('student/<str:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<str:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('educators/', EducatorListCreateView.as_view(), name='educator-list-create'),
    path('educator/<str:pk>/', EducatorDetailView.as_view(), name='educator-detail'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('department/<str:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('academic-years/', AcademicYearListCreateView.as_view(), name='academic-year-list-create'),
    path('academic-year/<str:pk>/', AcademicYearDetailView.as_view(), name='academic-year-detail'),
    path('semesters/', SemesterListCreateView.as_view(), name='semester-list-create'),
    path('semester/<str:pk>/', SemesterDetailView.as_view(), name='semester-detail'),
]