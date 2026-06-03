from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CandidateForm
from .models import Candidate


def candidates(request):
    candidates_qs = list(Candidate.objects.select_related('user'))
    return render(request, 'candidate/candidates.html', {'candidates': candidates_qs or fallback_candidates()})


def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate.objects.select_related('user'), pk=pk)
    return render(request, 'candidate/resume.html', {'candidate': candidate, 'skill_items': split_skills(candidate.skills)})


def candidate_demo_detail(request, slug):
    candidate = next((item for item in fallback_candidates() if item['slug'] == slug), None)
    return render(request, 'candidate/resume.html', {'candidate': candidate, 'skill_items': split_skills(candidate['skills']) if candidate else []})


@login_required
def candidate_dashboard(request):
    candidate = Candidate.objects.filter(user=request.user).first()
    applications = candidate.applications.select_related('job') if candidate else []
    return render(request, 'candidate/dashboard.html', {'candidate': candidate, 'applications': applications})


def fallback_candidates():
    return [
        {'slug': 'aarav-sharma', 'name': 'Aarav Sharma', 'role': 'Django Developer', 'email': 'aarav@example.com', 'phone': '+91 98765 43210', 'location': 'Bengaluru', 'skills': 'Django, REST APIs, SQL', 'education': 'B.Tech Computer Science', 'experience': '3 years building hiring dashboards and backend APIs.', 'summary': 'Backend-focused developer with strong Django, database, and deployment fundamentals.'},
        {'slug': 'meera-iyer', 'name': 'Meera Iyer', 'role': 'Frontend Engineer', 'email': 'meera@example.com', 'phone': '+91 98765 43211', 'location': 'Remote', 'skills': 'React, Bootstrap, UX, JavaScript', 'education': 'B.Des Interaction Design', 'experience': 'Frontend engineer focused on accessible UI.', 'summary': 'Frontend specialist who builds responsive interfaces with clean interaction design.'},
        {'slug': 'kabir-khan', 'name': 'Kabir Khan', 'role': 'Data Analyst', 'email': 'kabir@example.com', 'phone': '+91 98765 43212', 'location': 'Pune', 'skills': 'Python, Analytics, Excel, SQL', 'education': 'B.Sc Statistics', 'experience': 'Data analyst with internship experience.', 'summary': 'Analyst skilled at turning raw data into clear dashboards and hiring insights.'},
    ]


def split_skills(value):
    return [skill.strip() for skill in value.split(',') if skill.strip()]


@login_required
def edit_candidate_profile(request):
    candidate, created = Candidate.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
    )
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate profile updated successfully.')
            return redirect('candidate_dashboard')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'candidate/edit_profile.html', {'form': form})
