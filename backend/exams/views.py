from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Exam, Question, Choice, ExamAttempt, Answer
from .serializers import (ExamSerializer, ExamListSerializer, QuestionSerializer,
                           ExamAttemptSerializer, SubmitExamSerializer)


class ExamListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'course', 'institution']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Exam.objects.filter(
                course__students=user, status__in=['published', 'active', 'closed']
            )
        elif user.role == 'teacher':
            return Exam.objects.filter(created_by=user)
        return Exam.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExamListSerializer
        return ExamSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartExamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            exam = Exam.objects.get(pk=pk, status__in=['published', 'active'])
        except Exam.DoesNotExist:
            return Response({'detail': 'Exam not available.'}, status=404)

        attempt, created = ExamAttempt.objects.get_or_create(
            exam=exam, student=request.user
        )
        if not created and attempt.submitted_at:
            return Response({'detail': 'You have already submitted this exam.'}, status=400)

        serializer = ExamAttemptSerializer(attempt)
        # Return exam with questions
        exam_data = ExamSerializer(exam, context={'request': request}).data
        return Response({'attempt': serializer.data, 'exam': exam_data})


class SubmitExamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubmitExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attempt_id = serializer.validated_data['attempt_id']
        answers    = serializer.validated_data['answers']

        try:
            attempt = ExamAttempt.objects.get(pk=attempt_id, student=request.user)
        except ExamAttempt.DoesNotExist:
            return Response({'detail': 'Attempt not found.'}, status=404)

        if attempt.submitted_at:
            return Response({'detail': 'Already submitted.'}, status=400)

        total_score = 0
        for ans in answers:
            try:
                question = Question.objects.get(pk=ans.get('question_id'), exam=attempt.exam)
                answer_obj, _ = Answer.objects.get_or_create(attempt=attempt, question=question)

                if ans.get('choice_id'):
                    choice = Choice.objects.get(pk=ans['choice_id'], question=question)
                    answer_obj.selected_choice = choice
                    answer_obj.is_correct = choice.is_correct
                    answer_obj.marks_awarded = question.marks if choice.is_correct else 0
                    total_score += float(answer_obj.marks_awarded)
                elif ans.get('text_answer'):
                    answer_obj.text_answer = ans['text_answer']

                answer_obj.save()
            except (Question.DoesNotExist, Choice.DoesNotExist):
                continue

        time_taken = int((timezone.now() - attempt.started_at).total_seconds() / 60)
        attempt.score = total_score
        attempt.is_passed = total_score >= attempt.exam.pass_marks
        attempt.submitted_at = timezone.now()
        attempt.time_taken_mins = time_taken
        attempt.save()

        return Response({
            'score':     total_score,
            'total':     attempt.exam.total_marks,
            'pass_marks':attempt.exam.pass_marks,
            'is_passed': attempt.is_passed,
            'time_taken':time_taken,
        })


class ExamResultListView(generics.ListAPIView):
    serializer_class = ExamAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['exam']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return ExamAttempt.objects.filter(student=user)
        return ExamAttempt.objects.all()
