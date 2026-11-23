from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'company',
            'location',
            'salary',
            'job_type',
            'description',
            'required_skills',
        ]

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Enter job description'
            }),

            'required_skills': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter required skills'
            }),
        }