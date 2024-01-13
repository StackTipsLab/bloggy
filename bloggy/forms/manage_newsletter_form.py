from django import forms

from bloggy.models.newsletter import Newsletter


class ManageNewsLetterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get('instance')

    class Meta:
        model = Newsletter
        fields = [
            'title', 'url',
            'content',
            'publish_status',
            'send_to_users_only',
            'send_to_all'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter title'
            }),

            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter url'
            }),

            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': "url",
            }),

            'publish_status': forms.Select(attrs={'class': 'form-control'}),
            'receive_news_updates': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'receive_new_content': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

            'send_to_all': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input mx-2',
                }),

            'send_to_users_only': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input mx-2',
                }),

        }
