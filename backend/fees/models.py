from django.db import models
from users.models import User, Institution


class FeeCategory(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='fee_categories')
    name        = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.institution.name} – {self.name}"


class FeeStructure(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    category    = models.ForeignKey(FeeCategory, on_delete=models.CASCADE, related_name='structures')
    academic_year = models.CharField(max_length=20)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    due_date    = models.DateField()
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category.name} – {self.academic_year} – ₹{self.amount}"


class FeePayment(models.Model):
    STATUS = [('pending','Pending'), ('paid','Paid'), ('partial','Partial'), ('overdue','Overdue')]
    METHODS = [('cash','Cash'), ('online','Online'), ('cheque','Cheque'), ('dd','DD')]

    student     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fee_payments',
                                    limit_choices_to={'role': 'student'})
    structure   = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status      = models.CharField(max_length=10, choices=STATUS, default='pending')
    method      = models.CharField(max_length=10, choices=METHODS, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_at     = models.DateTimeField(null=True, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)
    remarks     = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_payments')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} – {self.structure.category.name} – {self.status}"
