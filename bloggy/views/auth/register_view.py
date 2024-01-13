from django.shortcuts import render, redirect, reverse
from django.views import View

from bloggy import settings
from bloggy.forms.signup_form import SignUpForm
from bloggy.services.email_service import send_html_email
from bloggy.services.token_service import create_token


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("index"))

        return render(request, 'auth/register.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            verification_token = create_token(user, token_type="signup")
            self.send_account_activation_email(request, user, verification_token)
            return redirect(reverse('login'))

        return render(request, 'auth/register.html', {'form': form})

    def send_account_activation_email(self, request, new_user, verification_token):
        subject = f'Welcome to {settings.SITE_TITLE}!'
        args = {
            "email_subject": subject,
            "user_name": new_user.name,
            "app_name": settings.SITE_TITLE,
            "verification_link": request.build_absolute_uri(reverse("activate_account", args=[
                verification_token.uuid,
                verification_token.token
            ]))
        }

        send_html_email(subject, [new_user.email], "email/account_activation_email.html", args)
