from django.urls import path
from .views import EducatorDetailView, EducatorListCreateView, StudentListCreateView, StudentDetailView, CourseListCreateView, CourseDetailView, DepartmentListCreateView, DepartmentDetailView
urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<str:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<str:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('educators/', EducatorListCreateView.as_view(), name='educator-list-create'),
    path('educators/<str:pk>/', EducatorDetailView.as_view(), name='educator-detail'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<str:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
]