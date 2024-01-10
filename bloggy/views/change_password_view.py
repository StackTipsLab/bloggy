from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from bloggy.forms.change_password_form import ChangePasswordForm


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('profile.account')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your password was successfully changed.')
        return response
