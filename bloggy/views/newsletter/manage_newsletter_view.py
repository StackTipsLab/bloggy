from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import FormView
from django.contrib import messages
from bloggy import settings
from bloggy.forms.manage_newsletter_form import ManageNewsLetterForm
from bloggy.models import User
from bloggy.models.newsletter import Newsletter
from bloggy.models.subscriber import Subscribers
from bloggy.services.email_service import send_html_email


class ManageNewsletterView(LoginRequiredMixin, FormView):
    template_name = 'pages/dashboard/manage_newsletter.html'
    newsletter_template = "email/weekly_newsletter.html"
    form_class = ManageNewsLetterForm

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        form = ManageNewsLetterForm(instance=get_object_or_404(Newsletter, id=id))
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        newsletter_id = self.kwargs.get('id')
        newsletter = get_object_or_404(Newsletter, id=newsletter_id)
        form = ManageNewsLetterForm(request.POST, instance=newsletter)
        if not form.is_valid():
            messages.error(request, 'Form submission failed. Please check the data.')
            return render(request, self.template_name, {'form': form, 'newsletter': newsletter})
        else:
            action = request.POST.get('action')
            if action == 'save':
                newsletter = self.handle_save_action(form, newsletter_id)
                messages.success(request, 'Newsletter updated successfully.')
                return render(request, self.template_name, {'form': form, 'newsletter': newsletter})

            elif action == 'publish':
                newsletter = self.handle_save_action(form, newsletter_id)
                self.handle_publish_action(newsletter)
                messages.success(request, 'Newsletter sent!')
                return redirect('dashboard.newsletter')

            return render(request, self.template_name, {'form': form, 'newsletter': newsletter})

    def handle_save_action(self, form, newsletter_id):
        json_content = form.cleaned_data['content']
        published_date = timezone.now()  # form.cleaned_data['published_date']
        title = form.cleaned_data['title']
        send_to_all = form.cleaned_data['send_to_all']
        send_to_users_only = form.cleaned_data['send_to_users_only']

        newsletter_args = {
            'site_url': settings.SITE_URL,
            'newsletter_date': published_date.strftime("%B %d, %Y"),
            'posts': json_content['posts'],
            'news': json_content['news']
        }
        content_html = render_to_string(self.newsletter_template, newsletter_args)
        data = {
            'title': title,
            'url': f'issue-{slugify(published_date.strftime("%b-%Y"))}',
            'content_html': content_html,
            'content': json_content,
            'publish_status': "DRAFT",
            'send_to_all': send_to_all,
            'send_to_users_only': send_to_users_only,
            'published_date': published_date

        }
        newsletter, created = Newsletter.objects.update_or_create(
            id=newsletter_id,
            defaults=data
        )
        return newsletter

    def handle_publish_action(self, newsletter):
        if newsletter.send_to_all:
            users = chain(User.objects.filter(is_active=True).all(), Subscribers.objects.all())
        elif newsletter.send_to_users_only:
            users = User.objects.filter(is_active=True).all()

        args = {
            'site_url': settings.SITE_URL,
            'newsletter_date': newsletter.published_date.strftime("%B %d, %Y"),
            'posts': newsletter.content['posts'],
            'news': newsletter.content['news']
        }

        for user in users:
            send_html_email(newsletter.title, [user.email], self.newsletter_template, args,
                            from_email=settings.DEFAULT_FROM_EMAIL)
            print(f"Sending email to {user.email}")
        newsletter.publish_status = 'LIVE'
        newsletter.save()
