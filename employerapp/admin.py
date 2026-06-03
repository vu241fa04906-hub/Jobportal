from django.contrib import admin

from .models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'full_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('company_name', 'full_name', 'email', 'phone', 'user__username')
