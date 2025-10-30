
from django.urls import path
from . import views

app_name = 'users'  # Ensure this is present

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home_view'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]