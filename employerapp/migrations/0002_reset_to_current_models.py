# Generated to replace older demo employer models with the current Employer model.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employerapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.DeleteModel(name='EmployerApplication'),
        migrations.DeleteModel(name='JobPosting'),
        migrations.DeleteModel(name='EmployerCompany'),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=160)),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('website', models.URLField(blank=True)),
                ('company_description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['company_name'],
            },
        ),
    ]
