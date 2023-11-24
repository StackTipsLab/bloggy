from django.contrib.auth.views import LoginView
from django.urls import reverse


class MyLoginView(LoginView):

    def get_success_url(self):
        redirect_url = self.request.GET.get('next')
        if redirect_url:
            return redirect_url

        return reverse('index')
