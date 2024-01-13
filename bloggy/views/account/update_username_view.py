from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model

from bloggy.forms.update_username_form import UpdateUsernameForm


class UpdateUsernameView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UpdateUsernameForm
    template_name = 'profile/update_username.html'
    success_url = reverse_lazy('profile.account')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your username was successfully updated.')
        return response
