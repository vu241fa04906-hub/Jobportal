from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class BootstrapMixin:
    def style_fields(self):
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('autocomplete', 'off')


class RegisterForm(BootstrapMixin, UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full name',
            'autocomplete': 'name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'autocomplete': 'email',
        })
    )
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
        })
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create password',
            'class': 'form-control password-input',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm password',
            'class': 'form-control password-input',
            'autocomplete': 'new-password',
        })

        for name, field in self.fields.items():
            if self.is_bound and self.errors.get(name):
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} is-invalid'.strip()

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class LoginForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control password-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class ProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'role', 'profile_image', 'phone', 'address', 'status')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Current address'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class StyledPasswordResetForm(BootstrapMixin, PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['email'].widget.attrs.update({'placeholder': 'Registered email'})


class StyledSetPasswordForm(BootstrapMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control password-input'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control password-input'})


class StyledPasswordChangeForm(BootstrapMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()
        for name in ('old_password', 'new_password1', 'new_password2'):
            self.fields[name].widget.attrs.update({'class': 'form-control password-input'})
