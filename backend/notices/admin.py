from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display  = ['title', 'institution', 'priority', 'target_audience', 'is_published', 'created_at']
    list_filter   = ['priority', 'is_published', 'target_audience']
    list_editable = ['is_published']
