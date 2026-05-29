from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Institution, StudentProfile, TeacherProfile, DemoRequest


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'institution', 'is_verified', 'date_joined']
    list_filter  = ['role', 'institution', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        ('RW EduPlatform', {'fields': ('role', 'phone', 'avatar', 'institution', 'is_verified')}),
    )


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'email', 'created_at']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'admission_date']
    search_fields = ['roll_number', 'user__first_name', 'user__last_name']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'designation']


@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone', 'created_at', 'contacted']
    list_editable = ['contacted']
