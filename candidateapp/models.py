from django.conf import settings
from django.db import models


class Candidate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=150, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name or self.user.get_full_name() or self.user.username

    def skill_list(self):
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
