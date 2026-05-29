from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',        views.DashboardStatsView.as_view(),  name='dashboard'),
    path('recent-activity/',  views.RecentActivityView.as_view(),  name='recent_activity'),
]
