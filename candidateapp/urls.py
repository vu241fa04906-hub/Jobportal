from django.urls import path

from . import views

urlpatterns = [
    path('', views.candidates, name='candidates'),
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('detail/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('demo/<slug:slug>/', views.candidate_demo_detail, name='candidate_demo_detail'),
    path('edit-profile/', views.edit_candidate_profile, name='edit_candidate_profile'),
]
