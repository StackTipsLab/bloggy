from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.utils import json

from bloggy import settings
from bloggy.services.email_service import send_plain_email
from bloggy.utils.string_utils import StringUtils


class FeedbackApi(viewsets.ViewSet):
    def feedback(self, request):
        message = request.POST["message"]

        honeypot = request.POST.get("honeypot", None)
        if honeypot:
            return HttpResponse(
                json.dumps({'success': False,
                            'message': "This is a community for learners! "
                                       "We encourage genuine engagement and learning. "
                                       "Please refrain from using automated bots or cheating methods. "
                                       "Let's keep this space focused on authentic educational experiences."}),
                content_type="application/json"
            )

        if StringUtils.is_not_blank(message):
            subject = 'New Feedback'
            message_content = (f'Name: {request.POST.get("name", "-")}'
                               f'\n\nEmail: {request.POST.get("email", "-")}'
                               f'\n\nMessage: {message}'
                               f'\n\nIs Bug: {request.POST.get("bug", "false")}'
                               f'\n\nKeep Me Informed: {request.POST.get("keepMeInformed", "false")}'
                               f'\n\nSource: {request.POST.get("source", "-")}'
                               f'\n\nSourceLink: {request.POST.get("sourceLink", "-")}')
            send_plain_email(subject, [settings.DEFAULT_FROM_EMAIL], message_content)
            return HttpResponse(
                json.dumps({'success': True, "message": "We have received your feedback. Thank you for your support!"}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({'success': False, 'message': "Please enter the message"}),
                content_type="application/json"
            )
