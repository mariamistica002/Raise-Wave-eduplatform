from rest_framework import serializers
from .models import FeeCategory, FeeStructure, FeePayment


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = FeeCategory
        fields = '__all__'


class FeeStructureSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model  = FeeStructure
        fields = '__all__'


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name   = serializers.CharField(source='student.get_full_name', read_only=True)
    category_name  = serializers.CharField(source='structure.category.name', read_only=True)
    total_amount   = serializers.DecimalField(source='structure.amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = FeePayment
        fields = '__all__'
        read_only_fields = ['recorded_by', 'created_at', 'receipt_number']

    def create(self, validated_data):
        import uuid
        validated_data['recorded_by'] = self.context['request'].user
        validated_data['receipt_number'] = f"RW{str(uuid.uuid4())[:8].upper()}"
        return super().create(validated_data)
