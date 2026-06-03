from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.signup, name='register'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.ResetPasswordView.as_view(), name='password_reset_confirm'),
    path('reset-password/', views.reset_password_simple, name='reset_password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
