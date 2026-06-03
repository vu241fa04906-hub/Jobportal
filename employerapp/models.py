from django.conf import settings
from django.db import models


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    full_name = models.CharField(max_length=150, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(blank=True)
    company_name = models.CharField(max_length=160)
    company_logo = models.FileField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name
