from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from users.models import User
from courses.models import Course
from attendance.models import Attendance, AttendanceSession
from exams.models import Exam, ExamAttempt
from fees.models import FeePayment
from notices.models import Notice
from django.db.models import Count, Avg, Sum
from django.utils import timezone
import datetime


class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'admin' or user.is_staff:
            # Admin dashboard
            inst = user.institution
            students_qs = User.objects.filter(role='student', institution=inst)
            teachers_qs = User.objects.filter(role='teacher', institution=inst)
            courses_qs  = Course.objects.filter(institution=inst)

            today = timezone.now().date()
            today_sessions = AttendanceSession.objects.filter(date=today, course__institution=inst)
            today_present  = Attendance.objects.filter(session__in=today_sessions, status__in=['present','late']).count()
            today_total    = Attendance.objects.filter(session__in=today_sessions).count()
            today_pct      = round(today_present / today_total * 100, 1) if today_total > 0 else 0

            total_fees_due  = FeePayment.objects.filter(student__institution=inst).aggregate(s=Sum('structure__amount'))['s'] or 0
            total_fees_paid = FeePayment.objects.filter(student__institution=inst).aggregate(s=Sum('amount_paid'))['s'] or 0

            return Response({
                'total_students': students_qs.count(),
                'total_teachers': teachers_qs.count(),
                'total_courses':  courses_qs.count(),
                'today_attendance_pct': today_pct,
                'active_exams':   Exam.objects.filter(institution=inst, status='active').count(),
                'pending_fees':   round(float(total_fees_due) - float(total_fees_paid), 2),
                'unread_notices': Notice.objects.filter(institution=inst, is_published=True).count(),
                'new_students_this_month': students_qs.filter(
                    date_joined__month=today.month, date_joined__year=today.year
                ).count(),
            })

        elif user.role == 'student':
            # Student dashboard
            enrolled = Course.objects.filter(students=user)
            attempts = ExamAttempt.objects.filter(student=user, submitted_at__isnull=False)
            avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0

            total_att = Attendance.objects.filter(student=user).count()
            present   = Attendance.objects.filter(student=user, status__in=['present','late']).count()
            att_pct   = round(present / total_att * 100, 1) if total_att > 0 else 0

            from fees.models import FeePayment
            pending_fees = FeePayment.objects.filter(student=user, status__in=['pending','overdue'])

            return Response({
                'enrolled_courses':    enrolled.count(),
                'completed_exams':     attempts.count(),
                'average_score':       round(float(avg_score), 1),
                'attendance_pct':      att_pct,
                'pending_fees_count':  pending_fees.count(),
                'upcoming_exams':      Exam.objects.filter(
                    course__students=user,
                    status__in=['published','active'],
                    end_time__gte=timezone.now()
                ).count(),
            })

        elif user.role == 'teacher':
            taught = Course.objects.filter(teacher=user)
            total_students = User.objects.filter(enrolled_courses__in=taught).distinct().count()
            exams_created  = Exam.objects.filter(created_by=user).count()

            return Response({
                'courses_taught':  taught.count(),
                'total_students':  total_students,
                'exams_created':   exams_created,
                'pending_grading': 0,  # extend as needed
            })

        return Response({'detail': 'No dashboard data available.'})


class RecentActivityView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notices = Notice.objects.filter(is_published=True).order_by('-created_at')[:5]
        return Response({
            'notices': [{'id': n.id, 'title': n.title, 'priority': n.priority, 'created_at': n.created_at} for n in notices]
        })
