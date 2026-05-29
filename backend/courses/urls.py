from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.CourseListCreateView.as_view(),    name='course_list'),
    path('<int:pk>/',                  views.CourseDetailView.as_view(),        name='course_detail'),
    path('<int:pk>/enroll/',           views.CourseEnrollView.as_view(),        name='course_enroll'),
    path('<int:course_pk>/topics/',    views.TopicListCreateView.as_view(),     name='topic_list'),
    path('<int:course_pk>/materials/', views.StudyMaterialListCreateView.as_view(), name='material_list'),
    path('materials/<int:pk>/',        views.StudyMaterialDetailView.as_view(), name='material_detail'),
    path('departments/',               views.DepartmentListCreateView.as_view(), name='department_list'),
    path('departments/<int:pk>/',      views.DepartmentDetailView.as_view(),    name='department_detail'),
]
