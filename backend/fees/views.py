from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import FeeCategory, FeeStructure, FeePayment
from .serializers import FeeCategorySerializer, FeeStructureSerializer, FeePaymentSerializer


class FeeCategoryListCreateView(generics.ListCreateAPIView):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institution']


class FeeStructureListCreateView(generics.ListCreateAPIView):
    queryset = FeeStructure.objects.filter(is_active=True)
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['institution', 'academic_year', 'category']


class FeePaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = FeePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'status', 'structure__category']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return FeePayment.objects.filter(student=user)
        return FeePayment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(recorded_by=self.request.user)
        if payment.amount_paid >= payment.structure.amount:
            payment.status = 'paid'
            payment.paid_at = timezone.now()
        elif payment.amount_paid > 0:
            payment.status = 'partial'
        payment.save()


class FeePaymentDetailView(generics.RetrieveUpdateAPIView):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentFeeSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        payments = FeePayment.objects.filter(student=user)
        total_due  = sum(p.structure.amount for p in payments)
        total_paid = sum(p.amount_paid for p in payments)
        return Response({
            'total_due':     float(total_due),
            'total_paid':    float(total_paid),
            'balance':       float(total_due - total_paid),
            'pending_count': payments.filter(status__in=['pending', 'overdue']).count(),
        })
