from django.contrib import admin
from .models import Exam, Question, Choice, ExamAttempt, Answer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'institution', 'status', 'start_time', 'end_time']
    list_filter  = ['status', 'institution']
    inlines      = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'text', 'question_type', 'marks', 'order']
    inlines      = [ChoiceInline]

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'score', 'is_passed', 'submitted_at']
