from django import forms


class CreateNewsletterForm(forms.Form):
    title = forms.CharField(
        label="Newsletter title",
        max_length=254,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Weekly newsletter'}),
    )

    # published_date = forms.DateTimeField(
    #     label="Published date",
    #     help_text="Date time for sending the newsletter",
    #     widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'})
    # )

    json_file = forms.FileField(
        label='Upload JSON File',
        help_text="Upload a valid json file",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    send_to_all = forms.BooleanField(
        label="Send to all",
        required=False,
        help_text="This newsletter will be send all users",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mx-2',
            }),
    )

    send_to_users_only = forms.BooleanField(
        label="Send to registered users only",
        required=False,
        help_text="This newsletter will be send only to registered users",
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mx-2',
            }),

    )
