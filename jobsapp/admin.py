from django.contrib import admin

from .models import Category, Job


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'experience_level', 'deadline', 'is_active')
    list_filter = ('job_type', 'experience_level', 'is_active', 'category')
    search_fields = ('title', 'location', 'description', 'employer__company_name')
