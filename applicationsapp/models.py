from django.db import models
from django.utils import timezone


class Application(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('review', 'In Review'),
        ('shortlisted', 'Shortlisted'),
        ('assessment', 'Assessment'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )

    candidate = models.ForeignKey('candidateapp.Candidate', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey('jobsapp.Job', on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f'{self.full_name} applied for {self.job}'
