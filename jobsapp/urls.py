from django.urls import path

from . import views

urlpatterns = [
    path('', views.jobs, name='jobs'),
    path('search/', views.search_results, name='search_results'),
    path('categories/', views.categories, name='categories'),
    path('categories/<str:key>/', views.category_detail, name='category_detail'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('post/', views.post_job, name='post_job'),
    path('<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('<int:pk>/delete/', views.delete_job, name='delete_job'),
]
