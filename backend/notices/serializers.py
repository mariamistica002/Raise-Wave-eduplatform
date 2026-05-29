from rest_framework import serializers
from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    published_by_name = serializers.CharField(source='published_by.get_full_name', read_only=True)

    class Meta:
        model  = Notice
        fields = '__all__'
        read_only_fields = ['published_by', 'created_at']
