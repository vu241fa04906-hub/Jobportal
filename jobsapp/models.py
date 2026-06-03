from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    image = models.FileField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
    )
    EXPERIENCE_CHOICES = (
        ('fresher', 'Fresher'),
        ('junior', 'Junior'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    )

    employer = models.ForeignKey('employerapp.Employer', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    title = models.CharField(max_length=180)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='jobs', null=True, blank=True)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=140)
    status = models.CharField(max_length=20, default='open')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
