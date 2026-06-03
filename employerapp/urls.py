from django.urls import path

from . import views

urlpatterns = [
    path('', views.employers, name='employers'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('detail/<int:pk>/', views.employer_detail, name='employer_detail'),
    path('demo/<slug:slug>/', views.employer_demo_detail, name='employer_demo_detail'),
    path('edit-profile/', views.edit_employer_profile, name='edit_employer_profile'),
]
