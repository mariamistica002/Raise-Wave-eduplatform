from django.db import models
from users.models import User, Institution
from courses.models import Course


class Exam(models.Model):
    STATUS = [('draft','Draft'), ('published','Published'), ('active','Active'), ('closed','Closed')]

    institution  = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='exams')
    course       = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams')
    title        = models.CharField(max_length=255)
    description  = models.TextField(blank=True)
    duration_mins= models.PositiveIntegerField(default=60)
    total_marks  = models.PositiveIntegerField(default=100)
    pass_marks   = models.PositiveIntegerField(default=40)
    start_time   = models.DateTimeField(null=True, blank=True)
    end_time     = models.DateTimeField(null=True, blank=True)
    status       = models.CharField(max_length=12, choices=STATUS, default='draft')
    shuffle_questions = models.BooleanField(default=False)
    show_result_immediately = models.BooleanField(default=True)
    created_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPES = [('mcq','MCQ'), ('truefalse','True/False'), ('short','Short Answer')]

    exam        = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text        = models.TextField()
    question_type = models.CharField(max_length=10, choices=TYPES, default='mcq')
    marks       = models.PositiveIntegerField(default=1)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}"


class Choice(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text       = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class ExamAttempt(models.Model):
    exam        = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts')
    student     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts')
    started_at  = models.DateTimeField(auto_now_add=True)
    submitted_at= models.DateTimeField(null=True, blank=True)
    score       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_passed   = models.BooleanField(null=True, blank=True)
    time_taken_mins = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['exam', 'student']

    def __str__(self):
        return f"{self.student} – {self.exam} – {self.score}"


class Answer(models.Model):
    attempt    = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer= models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    marks_awarded = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ['attempt', 'question']
