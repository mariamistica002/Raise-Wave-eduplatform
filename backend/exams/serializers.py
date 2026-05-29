from rest_framework import serializers
from .models import Exam, Question, Choice, ExamAttempt, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Choice
        fields = ['id', 'text', 'is_correct']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Hide correct answer from students during exam
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.role == 'student':
            data.pop('is_correct', None)
        return data


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model  = Question
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    questions    = QuestionSerializer(many=True, read_only=True)
    question_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model  = Exam
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']


class ExamListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(source='questions.count', read_only=True)

    class Meta:
        model  = Exam
        fields = ['id', 'title', 'duration_mins', 'total_marks', 'pass_marks',
                  'start_time', 'end_time', 'status', 'question_count']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Answer
        fields = ['question', 'selected_choice', 'text_answer']


class ExamAttemptSerializer(serializers.ModelSerializer):
    answers      = AnswerSerializer(many=True, read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title   = serializers.CharField(source='exam.title', read_only=True)

    class Meta:
        model  = ExamAttempt
        fields = '__all__'
        read_only_fields = ['student', 'started_at', 'score', 'is_passed', 'time_taken_mins']


class SubmitExamSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField()
    answers    = serializers.ListField(child=serializers.DictField())
