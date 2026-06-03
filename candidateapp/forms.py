from django import forms

from .models import Candidate


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('full_name', 'email', 'phone', 'address', 'skills', 'resume', 'education', 'experience', 'status')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, SQL, Bootstrap'}),
            'education': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
