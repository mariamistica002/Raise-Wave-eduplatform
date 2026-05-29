from rest_framework import serializers
from .models import AttendanceSession, Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model  = Attendance
        fields = '__all__'


class AttendanceSessionSerializer(serializers.ModelSerializer):
    records      = AttendanceSerializer(many=True, read_only=True)
    present_count= serializers.SerializerMethodField()
    absent_count = serializers.SerializerMethodField()

    class Meta:
        model  = AttendanceSession
        fields = '__all__'

    def get_present_count(self, obj):
        return obj.records.filter(status__in=['present', 'late']).count()

    def get_absent_count(self, obj):
        return obj.records.filter(status='absent').count()


class BulkAttendanceSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    records    = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )
