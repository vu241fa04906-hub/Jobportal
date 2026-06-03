from django.contrib import admin

from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'phone', 'skills', 'user__username')
