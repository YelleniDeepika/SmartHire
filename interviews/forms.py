from django import forms
from .models import Interview


class InterviewForm(forms.ModelForm):

    class Meta:
        model = Interview
        fields = [
            'interview_date',
            'interview_time',
            'mode',
            'meeting_link',
            'location',
            'notes',
        ]

        widgets = {
            'interview_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'interview_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter interview instructions or notes'
                }
            ),
        }