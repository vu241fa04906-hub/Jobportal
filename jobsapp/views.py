from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from employerapp.models import Employer
from .forms import JobForm
from .models import Category, Job


def fallback_jobs():
    return [
        {'id': 1, 'title': 'Senior Django Developer', 'company': 'CloudNova', 'location': 'Bengaluru', 'salary': '18-28 LPA', 'job_type': 'Full Time', 'experience_level': 'Senior', 'description': 'Build scalable hiring products with Django, APIs, and clean UI workflows.'},
        {'id': 2, 'title': 'Frontend Engineer', 'company': 'PixelWorks', 'location': 'Remote', 'salary': '10-18 LPA', 'job_type': 'Remote', 'experience_level': 'Mid Level', 'description': 'Create fast Bootstrap interfaces with polished JavaScript interactions.'},
        {'id': 3, 'title': 'Data Analyst Intern', 'company': 'InsightHub', 'location': 'Pune', 'salary': '25k/month', 'job_type': 'Internship', 'experience_level': 'Fresher', 'description': 'Turn business data into dashboards and hiring insights.'},
    ]


def jobs(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()
    jobs_qs = Job.objects.select_related('category', 'employer').filter(is_active=True)
    if query:
        jobs_qs = jobs_qs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(employer__company_name__icontains=query))
    if location:
        jobs_qs = jobs_qs.filter(location__icontains=location)
    jobs_data = list(jobs_qs)
    return render(request, 'jobs/jobs.html', {
        'jobs': jobs_data or fallback_jobs(),
        'query': query,
        'location': location,
        'categories': Category.objects.all(),
    })


def job_detail(request, pk):
    job_exists = Job.objects.filter(pk=pk).exists()
    if job_exists:
        job = get_object_or_404(Job, pk=pk)
    else:
        job = next((item for item in fallback_jobs() if item['id'] == pk), fallback_jobs()[0])
    return render(request, 'jobs/job_detail.html', {'job': job, 'can_apply': job_exists})


def categories(request):
    categories_qs = list(Category.objects.all())
    fallback = fallback_categories()
    return render(request, 'jobs/categories.html', {'categories': categories_qs or fallback})


def category_detail(request, key):
    category = None
    jobs_qs = []
    if key.isdigit():
        category = get_object_or_404(Category, pk=int(key))
        jobs_qs = Job.objects.select_related('employer').filter(category=category, is_active=True)
    else:
        category = next((item for item in fallback_categories() if item['slug'] == key), None)
        if not category:
            category = {'name': 'Category Not Found', 'description': 'The requested category could not be found.', 'icon': 'fa-layer-group', 'skills': []}

    return render(request, 'jobs/category_detail.html', {
        'category': category,
        'jobs': list(jobs_qs),
    })


def search_results(request):
    return jobs(request)


def fallback_categories():
    return [
        {'slug': 'design', 'name': 'Design', 'icon': 'fa-pen-nib', 'description': 'UI, UX, product design, brand systems, and creative roles.', 'skills': ['Figma', 'UX Research', 'Design Systems']},
        {'slug': 'development', 'name': 'Development', 'icon': 'fa-code', 'description': 'Frontend, backend, full stack, mobile, and platform engineering jobs.', 'skills': ['Django', 'React', 'APIs']},
        {'slug': 'marketing', 'name': 'Marketing', 'icon': 'fa-bullhorn', 'description': 'Growth, content, SEO, campaign, and performance marketing careers.', 'skills': ['SEO', 'Content', 'Analytics']},
        {'slug': 'data-science', 'name': 'Data Science', 'icon': 'fa-chart-line', 'description': 'Analytics, machine learning, data engineering, and BI opportunities.', 'skills': ['Python', 'SQL', 'Dashboards']},
        {'slug': 'finance', 'name': 'Finance', 'icon': 'fa-coins', 'description': 'Accounting, financial analysis, operations, and fintech roles.', 'skills': ['Excel', 'Reporting', 'Forecasting']},
        {'slug': 'human-resources', 'name': 'Human Resources', 'icon': 'fa-users', 'description': 'Recruiting, people operations, HR coordination, and talent roles.', 'skills': ['Hiring', 'Onboarding', 'Communication']},
        {'slug': 'operations', 'name': 'Operations', 'icon': 'fa-gears', 'description': 'Process, support, business operations, and program management roles.', 'skills': ['Planning', 'Support', 'Process']},
        {'slug': 'sales', 'name': 'Sales', 'icon': 'fa-handshake', 'description': 'Inside sales, business development, account management, and revenue roles.', 'skills': ['CRM', 'Negotiation', 'Prospecting']},
    ]


@login_required
def post_job(request):
    employer = Employer.objects.filter(user=request.user).first()
    if not employer:
        messages.warning(request, 'Please complete your employer profile before posting a job.')
        return redirect('edit_employer_profile')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, 'Job posted successfully.')
            return redirect('employer_dashboard')
    else:
        form = JobForm(initial={'employer': employer})
        if 'employer' in form.fields:
            form.fields['employer'].widget = forms.HiddenInput()
            
    return render(request, 'jobs/post_job.html', {'form': form, 'title': 'Post a Job'})


@login_required
def edit_job(request, pk):
    employer = Employer.objects.filter(user=request.user).first()
    if not employer:
        messages.warning(request, 'Please complete your employer profile.')
        return redirect('edit_employer_profile')
        
    job = get_object_or_404(Job, pk=pk, employer=employer)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)
        if 'employer' in form.fields:
            form.fields['employer'].widget = forms.HiddenInput()
            
    return render(request, 'jobs/post_job.html', {'form': form, 'title': 'Edit Job'})


@login_required
def delete_job(request, pk):
    employer = Employer.objects.filter(user=request.user).first()
    if not employer:
        return redirect('login')
    job = get_object_or_404(Job, pk=pk, employer=employer)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('employer_dashboard')
    return render(request, 'jobs/delete_job.html', {'job': job})
