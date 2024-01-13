from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views import View

from bloggy import settings
from bloggy.models import User
from bloggy.services.token_service import get_token, is_token_expired


class AccountActivationView(View):
    def get(self, request, uuid, token):
        verification_token = get_token(uuid, token, token_type="signup")
        if is_token_expired(verification_token):
            messages.error(request, "The verification link is expired or malformed.")
            return redirect('index')

        # activate user
        user = User.objects.get(email=verification_token.user.email)
        user.is_active = True
        user.is_staff = False
        group = Group.objects.get_or_create(name=settings.AUTH_USER_DEFAULT_GROUP)
        user.groups.add(group[0].id)
        user.save()

        # delete token as it
        verification_token.delete()

        messages.success(request, "You're all set! Your account is now active and ready to use.")
        return redirect('login')
