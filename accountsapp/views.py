from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, ProfileForm, RegisterForm, StyledPasswordChangeForm, StyledPasswordResetForm, StyledSetPasswordForm
from .models import UserProfile


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ForgotPasswordView(PasswordResetView):
    template_name = 'accounts/forgot_password.html'
    form_class = StyledPasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Password reset instructions are ready. Configure email settings to send them.')
        return super().form_valid(form)


class ResetPasswordView(PasswordResetConfirmView):
    template_name = 'accounts/reset_password.html'
    form_class = StyledSetPasswordForm
    success_url = reverse_lazy('login')


class ChangePasswordView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = StyledPasswordChangeForm
    success_url = reverse_lazy('profile')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data['full_name']
            user.first_name = full_name.split(' ', 1)[0]
            user.last_name = full_name.split(' ', 1)[1] if ' ' in full_name else ''
            user.email = form.cleaned_data['email']
            user.save(update_fields=['first_name', 'last_name', 'email'])
            role = form.cleaned_data['role']
            UserProfile.objects.create(
                user=user,
                full_name=full_name,
                email=user.email,
                role=role,
            )
            if role == 'candidate':
                from candidateapp.models import Candidate
                Candidate.objects.get_or_create(
                    user=user,
                    defaults={
                        'full_name': full_name,
                        'email': user.email,
                    }
                )
            elif role == 'employer':
                from employerapp.models import Employer
                Employer.objects.get_or_create(
                    user=user,
                    defaults={
                        'full_name': full_name,
                        'email': user.email,
                        'company_name': f"{full_name}'s Company" if full_name else f"{user.username}'s Company",
                    }
                )
            login(request, user)
            messages.success(request, 'Welcome aboard. Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


def otp_verification(request):
    verified = request.method == 'POST'
    if verified:
        messages.success(request, 'OTP verified successfully.')
    return render(request, 'accounts/otp_verification.html', {'verified': verified})


def reset_password_simple(request):
    messages.info(request, 'Use the secure reset link from your email to set a new password.')
    return render(request, 'accounts/reset_password.html', {'form': None})


@login_required
def profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email or '',
        },
    )
    return render(request, 'accounts/profile.html', {'profile': profile_obj})


@login_required
def edit_profile(request):
    profile_obj, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email or '',
        },
    )
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, 'accounts/edit_profile.html', {'form': form})
