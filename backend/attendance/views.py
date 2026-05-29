from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import AttendanceSession, Attendance
from .serializers import AttendanceSessionSerializer, AttendanceSerializer, BulkAttendanceSerializer
from users.models import User


class AttendanceSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return AttendanceSession.objects.filter(course__students=user)
        elif user.role == 'teacher':
            return AttendanceSession.objects.filter(taken_by=user)
        return AttendanceSession.objects.all()

    def perform_create(self, serializer):
        session = serializer.save(taken_by=self.request.user)
        # Auto-create absent records for all enrolled students
        course = session.course
        for student in course.students.all():
            Attendance.objects.get_or_create(session=session, student=student,
                                              defaults={'status': 'absent'})


class AttendanceSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class BulkAttendanceView(APIView):
    """Mark attendance for all students in one request."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data['session_id']
        records    = serializer.validated_data['records']

        try:
            session = AttendanceSession.objects.get(pk=session_id)
        except AttendanceSession.DoesNotExist:
            return Response({'detail': 'Session not found.'}, status=404)

        updated = 0
        for rec in records:
            student_id = rec.get('student_id')
            att_status = rec.get('status', 'absent')
            if student_id:
                Attendance.objects.update_or_create(
                    session=session, student_id=student_id,
                    defaults={'status': att_status, 'remark': rec.get('remark', '')}
                )
                updated += 1

        return Response({'detail': f'Attendance marked for {updated} students.'})


class StudentAttendanceSummaryView(APIView):
    """Return attendance % per course for a student."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id=None):
        student = request.user if student_id is None else User.objects.get(pk=student_id)
        from courses.models import Course
        summary = []
        for course in Course.objects.filter(students=student):
            total    = Attendance.objects.filter(session__course=course, student=student).count()
            present  = Attendance.objects.filter(session__course=course, student=student,
                                                  status__in=['present', 'late']).count()
            percentage = round((present / total * 100), 1) if total > 0 else 0
            summary.append({
                'course_id':   course.id,
                'course_name': course.name,
                'course_code': course.code,
                'total':       total,
                'present':     present,
                'percentage':  percentage,
            })
        return Response(summary)
