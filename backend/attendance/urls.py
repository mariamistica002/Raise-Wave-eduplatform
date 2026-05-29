from django.urls import path
from . import views

urlpatterns = [
    path('sessions/',                    views.AttendanceSessionListCreateView.as_view(), name='session_list'),
    path('sessions/<int:pk>/',           views.AttendanceSessionDetailView.as_view(),     name='session_detail'),
    path('bulk/',                        views.BulkAttendanceView.as_view(),              name='bulk_attendance'),
    path('summary/',                     views.StudentAttendanceSummaryView.as_view(),    name='my_summary'),
    path('summary/<int:student_id>/',    views.StudentAttendanceSummaryView.as_view(),    name='student_summary'),
]
