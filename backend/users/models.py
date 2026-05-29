from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent',  'Parent'),
    ]

    role        = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone       = models.CharField(max_length=20, blank=True)
    avatar      = models.ImageField(upload_to='avatars/', null=True, blank=True)
    institution = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    is_verified = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class Institution(models.Model):
    name       = models.CharField(max_length=255)
    code       = models.CharField(max_length=20, unique=True)
    address    = models.TextField(blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    email      = models.EmailField(blank=True)
    logo       = models.ImageField(upload_to='logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number     = models.CharField(max_length=30, unique=True)
    admission_date  = models.DateField(null=True, blank=True)
    date_of_birth   = models.DateField(null=True, blank=True)
    guardian_name   = models.CharField(max_length=150, blank=True)
    guardian_phone  = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    blood_group     = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"Profile: {self.user}"


class TeacherProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    department  = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    joining_date= models.DateField(null=True, blank=True)
    qualification = models.TextField(blank=True)

    def __str__(self):
        return f"Teacher: {self.user}"


class DemoRequest(models.Model):
    email      = models.EmailField()
    name       = models.CharField(max_length=150, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    message    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contacted  = models.BooleanField(default=False)

    def __str__(self):
        return self.email
