from django import forms
from django.forms import ClearableFileInput

from bloggy.models import User


class NonClearableFileInput(ClearableFileInput):
    template_name = 'forms/widgets/non_clearable_imagefield.html'


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts={
            "bio": "This will be displayed publicly on your profile. Keep it short and crisp."
        }
        fields = [
            'profile_photo',
            'name',
            'website',
            'twitter',
            'linkedin',
            'youtube',
            'github',
            'bio'
        ]

        widgets = {
            'profile_photo': NonClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter first name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "About you"
            }),
            'website': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your website'
            }),
            'twitter': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your twitter'
            }),
            'linkedin': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your linkedin'
            }),
            'youtube': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your youtube channel link'
            }),
            'github': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your github'
            }),
        }
