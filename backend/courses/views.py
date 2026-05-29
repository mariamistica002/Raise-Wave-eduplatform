from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Department, Course, Topic, StudyMaterial
from .serializers import (DepartmentSerializer, CourseSerializer,
                           CourseListSerializer, TopicSerializer, StudyMaterialSerializer)


class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ['teacher', 'admin'] or request.user.is_staff


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsTeacherOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institution']


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsTeacherOrAdmin]


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['institution', 'department', 'is_active', 'teacher']
    search_fields = ['name', 'code', 'description']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Course.objects.filter(students=user, is_active=True)
        elif user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        return Course.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseListSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseEnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=404)
        course.students.add(request.user)
        return Response({'detail': f'Enrolled in {course.name}.'})

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=404)
        course.students.remove(request.user)
        return Response({'detail': f'Unenrolled from {course.name}.'})


class TopicListCreateView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        return Topic.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])


class StudyMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsTeacherOrAdmin]

    def get_queryset(self):
        return StudyMaterial.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'], uploaded_by=self.request.user)


class StudyMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsTeacherOrAdmin]
