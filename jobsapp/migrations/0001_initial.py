# Generated to match the current jobsapp models.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employerapp', '0002_reset_to_current_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('salary', models.CharField(blank=True, max_length=80)),
                ('location', models.CharField(max_length=140)),
                ('experience_level', models.CharField(choices=[('fresher', 'Fresher'), ('junior', 'Junior'), ('mid', 'Mid Level'), ('senior', 'Senior'), ('lead', 'Lead')], default='fresher', max_length=20)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('internship', 'Internship'), ('contract', 'Contract'), ('remote', 'Remote')], default='full_time', max_length=20)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs', to='jobsapp.category')),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='employerapp.employer')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
