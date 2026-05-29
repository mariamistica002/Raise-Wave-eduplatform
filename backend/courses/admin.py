from django.contrib import admin
from .models import Department, Course, Topic, StudyMaterial

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'institution']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['name', 'code', 'teacher', 'institution', 'is_active']
    list_filter   = ['is_active', 'institution']
    filter_horizontal = ['students']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_completed']

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'material_type', 'uploaded_by', 'uploaded_at']
