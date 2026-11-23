
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=[
            ('recruiter', 'Recruiter'),
            ('candidate', 'Candidate'),
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'role',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email
