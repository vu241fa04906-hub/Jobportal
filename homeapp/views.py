from django.shortcuts import render

from jobsapp.views import fallback_jobs


def home(request):
    return render(request, 'home/home.html', {'featured_jobs': fallback_jobs()})


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    sent = request.method == 'POST'
    return render(request, 'home/contact.html', {'sent': sent})


def faq(request):
    return render(request, 'home/faq.html')


def testimonials(request):
    return render(request, 'home/testimonials.html')


def pricing(request):
    return render(request, 'home/pricing.html')


def error_404(request, exception=None):
    return render(request, 'home/404.html', status=404)


def error_500(request):
    return render(request, 'home/500.html', status=500)
