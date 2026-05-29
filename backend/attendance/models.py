from django.db import models
from users.models import User, Institution
from courses.models import Course


class AttendanceSession(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date        = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField(null=True, blank=True)
    topic       = models.CharField(max_length=255, blank=True)
    taken_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sessions_taken')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'date', 'start_time']
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.course.code} – {self.date}"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
        ('excused', 'Excused'),
    ]
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records',
                                 limit_choices_to={'role': 'student'})
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    remark  = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f"{self.student} – {self.session} – {self.status}"
