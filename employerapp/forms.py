from django import forms

from .models import Employer


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = (
            'full_name',
            'email',
            'phone',
            'address',
            'company_name',
            'company_logo',
            'website',
            'company_description',
            'status',
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'company_description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
