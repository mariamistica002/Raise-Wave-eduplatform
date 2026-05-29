from django.db import models
from users.models import User, Institution


class Department(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='departments')
    name        = models.CharField(max_length=150)
    code        = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.institution.name} – {self.name}"


class Course(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    department  = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    name        = models.CharField(max_length=255)
    code        = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    teacher     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taught_courses',
                                    limit_choices_to={'role': 'teacher'})
    students    = models.ManyToManyField(User, related_name='enrolled_courses', blank=True,
                                         limit_choices_to={'role': 'student'})
    start_date  = models.DateField(null=True, blank=True)
    end_date    = models.DateField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} – {self.name}"


class Topic(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_completed= models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class StudyMaterial(models.Model):
    MATERIAL_TYPES = [
        ('pdf',   'PDF'),
        ('video', 'Video'),
        ('link',  'External Link'),
        ('image', 'Image'),
        ('doc',   'Document'),
    ]
    course       = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    topic        = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    title        = models.CharField(max_length=255)
    material_type= models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file         = models.FileField(upload_to='materials/', null=True, blank=True)
    url          = models.URLField(blank=True)
    uploaded_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
