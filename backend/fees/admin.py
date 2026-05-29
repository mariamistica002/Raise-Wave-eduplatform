from django.contrib import admin
from .models import FeeCategory, FeeStructure, FeePayment

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution']

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['category', 'academic_year', 'amount', 'due_date', 'is_active']
    list_filter  = ['is_active', 'academic_year']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'structure', 'amount_paid', 'status', 'paid_at', 'receipt_number']
    list_filter  = ['status', 'method']
    search_fields= ['receipt_number', 'student__first_name']
