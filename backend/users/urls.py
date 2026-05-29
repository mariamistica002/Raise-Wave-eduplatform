from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/',           views.LoginView.as_view(),              name='login'),
    path('register/',        views.RegisterView.as_view(),           name='register'),
    path('logout/',          views.LogoutView.as_view(),             name='logout'),
    path('token/refresh/',   TokenRefreshView.as_view(),             name='token_refresh'),
    path('me/',              views.MeView.as_view(),                 name='me'),
    path('change-password/', views.ChangePasswordView.as_view(),     name='change_password'),
    path('users/',           views.UserListView.as_view(),           name='user_list'),
    path('users/<int:pk>/',  views.UserDetailView.as_view(),         name='user_detail'),
    path('institutions/',    views.InstitutionListCreateView.as_view(), name='institutions'),
    path('institutions/<int:pk>/', views.InstitutionDetailView.as_view(), name='institution_detail'),
    path('demo-request/',    views.DemoRequestView.as_view(),        name='demo_request'),
]
