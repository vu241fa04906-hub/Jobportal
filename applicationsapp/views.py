from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from candidateapp.models import Candidate
from employerapp.models import Employer
from jobsapp.models import Job
from .forms import ApplicationForm
from .models import Application


@login_required
def applications(request):
    user_profile = getattr(request.user, 'profile', None)
    if user_profile and user_profile.role == 'employer':
        employer = Employer.objects.filter(user=request.user).first()
        if employer:
            applications_qs = Application.objects.filter(job__employer=employer).select_related('candidate__user', 'job')
        else:
            applications_qs = Application.objects.none()
    else:
        candidate = Candidate.objects.filter(user=request.user).first()
        if candidate:
            applications_qs = Application.objects.filter(candidate=candidate).select_related('job', 'job__employer')
        else:
            applications_qs = Application.objects.none()

    return render(request, 'applications/applications.html', {'applications': applications_qs})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job.objects.select_related('employer'), pk=job_id, is_active=True)
    candidate = Candidate.objects.filter(user=request.user).first()
    initial = {
        'full_name': candidate.full_name if candidate else request.user.get_full_name() or request.user.username,
        'email': candidate.email if candidate else request.user.email,
        'phone': candidate.phone if candidate else '',
        'address': candidate.address if candidate else '',
        'skills': candidate.skills if candidate else '',
    }

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            candidate, _ = Candidate.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': form.cleaned_data['full_name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone'],
                    'address': form.cleaned_data['address'],
                    'skills': form.cleaned_data['skills'],
                    'resume': form.cleaned_data['resume'],
                },
            )
            application = form.save(commit=False)
            application.candidate = candidate
            application.job = job
            try:
                application.save()
            except IntegrityError:
                messages.warning(request, 'You have already applied for this job.')
                return redirect('candidate_dashboard')
            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('candidate_dashboard')
    else:
        form = ApplicationForm(initial=initial)

    return render(request, 'applications/apply_job.html', {'form': form, 'job': job})
