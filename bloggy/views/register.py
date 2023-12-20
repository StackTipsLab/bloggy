from django.shortcuts import render, redirect, reverse
from django.views import View

from bloggy.forms.signup_form import SignUpForm
from bloggy.services import email_service
from bloggy.services.token_service import create_token


class RegisterView(View):

    def get(self, request):
        return render(request, 'auth/register.html', {'form': SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            verification_token = create_token(user, token_type="signup")
            email_service.send_account_activation_email(request, user, verification_token)
            return redirect(reverse('login'))

        return render(request, 'auth/register.html', {'form': form})
