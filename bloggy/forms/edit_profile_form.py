from django import forms

from bloggy.forms.custom_input_fields import NonClearableFileInput
from bloggy.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        help_texts = {
            "bio": "This will be displayed publicly on your profile. Keep it short and crisp.",
            'receive_news_updates': "News about product and feature updates",
            'receive_new_content': "Get notified when new content is added"
        }

        labels = {
            'receive_news_updates': "News and updates",
            'receive_new_content': "New tutorials & courses"
        }

        fields = [
            'profile_photo', 'name', 'website', 'twitter', 'linkedin', 'youtube', 'github', 'bio',
            'receive_news_updates', 'receive_new_content'
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

            'receive_news_updates': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'receive_new_content': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

        }
