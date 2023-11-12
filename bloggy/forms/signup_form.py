from django.contrib.auth.forms import UserCreationForm

from bloggy.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)  # Call the parent class's save method
        # Generate the username based on the user's name (you can use your custom function here)
        user.username = self.generate_unique_username(self.cleaned_data['name'])
        user.is_active = False
        user.is_staff = False

        if commit:
            user.save()
        return user

    @staticmethod
    def generate_unique_username(name):
        # Convert the user's name to a lowercase username with underscores
        base_username = name.lower().replace(' ', '_')

        # Check if the base_username is unique, if not, append a number until it is
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        return username
