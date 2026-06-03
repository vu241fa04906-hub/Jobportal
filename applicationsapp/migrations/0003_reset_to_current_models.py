# Generated to replace older demo application models with the current Application model.

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationsapp', '0002_jobapplication'),
        ('candidateapp', '0002_reset_to_current_models'),
        ('jobsapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(name='JobApplication'),
        migrations.DeleteModel(name='Application'),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('review', 'In Review'), ('shortlisted', 'Shortlisted'), ('assessment', 'Assessment'), ('rejected', 'Rejected'), ('hired', 'Hired')], default='review', max_length=20)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='candidateapp.candidate')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobsapp.job')),
            ],
            options={
                'ordering': ['-applied_at'],
                'unique_together': {('candidate', 'job')},
            },
        ),
    ]
