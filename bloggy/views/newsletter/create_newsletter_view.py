import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from django.views import View
from bloggy import settings
from bloggy.forms.create_newsletter_form import CreateNewsletterForm
from bloggy.models.newsletter import Newsletter

class CreateNewsletterView(LoginRequiredMixin, View):
    template_name = 'pages/dashboard/create_newsletter.html'
    newsletter_template = "email/weekly_newsletter.html"

    def get(self, request, *args, **kwargs):
        form = CreateNewsletterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateNewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            published_date = datetime.now()
            title = form.cleaned_data['title']
            send_to_all = form.cleaned_data['send_to_all']
            send_to_users_only = form.cleaned_data['send_to_users_only']

            try:
                uploaded_file = request.FILES['json_file']
                json_content = json.loads(uploaded_file.read().decode('utf-8'))

                newsletter_args = {
                    'site_url': settings.SITE_URL,
                    'newsletter_date': published_date.strftime("%B %d, %Y"),
                    'posts': json_content['posts'],
                    'news': json_content['news']
                }
                content_html = render_to_string(self.newsletter_template, newsletter_args)

                Newsletter.objects.get_or_create(
                    title=title,
                    url=f'issue-{slugify(published_date.strftime("%d-%b-%Y"))}',
                    content_html=content_html,
                    content=json_content,
                    publish_status="DRAFT",
                    send_to_all=send_to_all,
                    send_to_users_only=send_to_users_only
                )

                messages.success(request, 'Newsletter uploaded successfully.')
                return render(
                    request,
                    self.template_name,
                    {'form': CreateNewsletterForm()})

            except Exception as e:
                messages.error(request, f'Error reading JSON file: {str(e)}')

        messages.error(request, 'Form submission failed. Please check the data.')
        return render(request, self.template_name, {'form': form})
