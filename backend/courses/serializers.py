from rest_framework import serializers
from .models import Department, Course, Topic, StudyMaterial
from users.serializers import UserSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Department
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Topic
        fields = '__all__'


class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StudyMaterial
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'uploaded_at']


class CourseSerializer(serializers.ModelSerializer):
    teacher_name   = serializers.CharField(source='teacher.get_full_name', read_only=True)
    student_count  = serializers.IntegerField(source='students.count', read_only=True)
    topics         = TopicSerializer(many=True, read_only=True)
    department_name= serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model  = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    teacher_name  = serializers.CharField(source='teacher.get_full_name', read_only=True)
    student_count = serializers.IntegerField(source='students.count', read_only=True)

    class Meta:
        model  = Course
        fields = ['id', 'name', 'code', 'description', 'teacher', 'teacher_name',
                  'student_count', 'is_active', 'start_date', 'end_date']
