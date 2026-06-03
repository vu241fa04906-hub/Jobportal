from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployerForm
from .models import Employer


def employers(request):
    employers_qs = list(Employer.objects.all())
    return render(request, 'employer/employers.html', {'employers': employers_qs or fallback_employers()})


def employer_detail(request, pk):
    employer = get_object_or_404(Employer.objects.select_related('user'), pk=pk)
    jobs = employer.jobs.filter(is_active=True)
    return render(request, 'employer/company_details.html', {'employer': employer, 'jobs': jobs})


def employer_demo_detail(request, slug):
    employer = next((item for item in fallback_employers() if item['slug'] == slug), None)
    return render(request, 'employer/company_details.html', {'employer': employer, 'jobs': []})


@login_required
def employer_dashboard(request):
    employer = Employer.objects.filter(user=request.user).first()
    jobs = employer.jobs.all() if employer else []
    return render(request, 'employer/dashboard.html', {'employer': employer, 'jobs': jobs})


def fallback_employers():
    return [
        {'slug': 'cloudnova', 'company_name': 'CloudNova', 'industry': 'Cloud Software', 'location': 'Bengaluru', 'open_roles': '12 open roles', 'company_description': 'CloudNova builds hiring tools for modern engineering teams and needs Django, DevOps, and product talent.', 'website': 'https://example.com'},
        {'slug': 'pixelworks', 'company_name': 'PixelWorks', 'industry': 'Product Design', 'location': 'Remote', 'open_roles': '8 open roles', 'company_description': 'PixelWorks is a design-led product studio hiring frontend engineers, UI designers, and UX researchers.', 'website': 'https://example.com'},
        {'slug': 'insighthub', 'company_name': 'InsightHub', 'industry': 'Data Analytics', 'location': 'Pune', 'open_roles': '6 open roles', 'company_description': 'InsightHub turns business data into dashboards, hiring intelligence, and actionable analytics.', 'website': 'https://example.com'},
    ]


@login_required
def edit_employer_profile(request):
    employer, created = Employer.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'company_name': f"{request.user.username}'s Company",
        }
    )
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employer profile updated successfully.')
            return redirect('employer_dashboard')
    else:
        form = EmployerForm(instance=employer)
    return render(request, 'employer/edit_profile.html', {'form': form})
