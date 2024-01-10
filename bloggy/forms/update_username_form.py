from django import forms
from django.contrib.auth import get_user_model


class UpdateUsernameForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']
        help_texts={
            'username': 'Letters, digits and "_" only allowed.'
        }
        labels = {
            "username": "New username",
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
        }

    def clean_username(self):
        new_username = self.cleaned_data['username']
        user_model = get_user_model()

        # Check if the new username is available
        if user_model.objects.filter(username=new_username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This username is already in use. Please choose a different one.')

        return new_username
