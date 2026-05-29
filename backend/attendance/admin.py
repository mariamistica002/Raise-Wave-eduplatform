from django.contrib import admin
from .models import AttendanceSession, Attendance

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['course', 'date', 'start_time', 'taken_by']
    list_filter  = ['date', 'course']
    raw_id_fields = ['taken_by', 'course']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status']
    list_filter  = ['status']
    raw_id_fields = ['student', 'session']