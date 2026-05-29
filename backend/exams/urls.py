from django.urls import path
from . import views

urlpatterns = [
    path('',              views.ExamListCreateView.as_view(), name='exam_list'),
    path('<int:pk>/',      views.ExamDetailView.as_view(),    name='exam_detail'),
    path('<int:pk>/start/',views.StartExamView.as_view(),     name='start_exam'),
    path('submit/',        views.SubmitExamView.as_view(),    name='submit_exam'),
    path('results/',       views.ExamResultListView.as_view(),name='exam_results'),
]
