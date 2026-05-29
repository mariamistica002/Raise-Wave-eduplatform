from django.urls import path
from . import views

urlpatterns = [
    path('categories/',        views.FeeCategoryListCreateView.as_view(),   name='fee_categories'),
    path('structures/',        views.FeeStructureListCreateView.as_view(),  name='fee_structures'),
    path('payments/',          views.FeePaymentListCreateView.as_view(),    name='fee_payments'),
    path('payments/<int:pk>/', views.FeePaymentDetailView.as_view(),        name='fee_payment_detail'),
    path('summary/',           views.StudentFeeSummaryView.as_view(),       name='fee_summary'),
]
