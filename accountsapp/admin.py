from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'user', 'role', 'phone', 'status', 'created_at')
    list_filter = ('role', 'status')
    search_fields = ('full_name', 'email', 'user__username', 'user__email', 'phone')
