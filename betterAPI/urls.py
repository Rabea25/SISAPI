from django.urls import path
from . import views
urlpatterns = [
    path('students/', views.StudentListCreateView.as_view(), name='student-list-create'),
    path('student/<str:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('courses/', views.CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<str:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('educators/', views.EducatorListCreateView.as_view(), name='educator-list-create'),
    path('educator/<str:pk>/', views.EducatorDetailView.as_view(), name='educator-detail'),
    path('departments/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('department/<str:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('academic-years/', views.AcademicYearListCreateView.as_view(), name='academic-year-list-create'),
    path('academic-year/<str:pk>/', views.AcademicYearDetailView.as_view(), name='academic-year-detail'),
    path('semesters/', views.SemesterListCreateView.as_view(), name='semester-list-create'),
    path('semester/<str:pk>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    path('user/create/', views.UserCreateView.as_view(), name='user-create'),
]