from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import json

from bloggy.models.subscriber import Subscribers
from bloggy.services import token_service
from bloggy.services.email_service import send_newsletter_verification_token


class SubscriberSerializer(ModelSerializer):
    class Meta:
        model = Subscribers
        fields = [
            'id',
            'email',
            'name',
            'created_date',
            'updated_date',
            'is_active',
        ]


class NewsletterApi(viewsets.ViewSet):

    def subscribe(self, request):
        json_body = request.data
        try:
            token = token_service.generate_verification_code()
            subscriber = Subscribers.objects.create(
                email=json_body.get('email'),
                name=json_body.get('name'),
                created_date=timezone.now(),
                confirmation_code=token,
                confirmed=False,
            )
            send_newsletter_verification_token(request, subscriber.email, subscriber.id, token)
        except IntegrityError:
            return HttpResponse(
                status=208,
                content=json.dumps({"error": "Already subscribed"}),
                content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"result": "successful"}),
            content_type="application/json"
        )

    def confirm(self, request, subscriber_id, token):
        subscriber = (Subscribers.objects.filter(id=subscriber_id).filter(confirmation_code=token).first())
        if subscriber is None:
            messages.error(request, "The verification link is expired or malformed.")
        elif subscriber.confirmed:
            messages.success(request, "You are already verified to receive updates from us.")
        else:
            subscriber.confirmed = True
            subscriber.confirmation_code = None
            subscriber.save()
            messages.success(request,
                             "Thank you for verifying your email.  "
                             "Now we will send you weekly tutorials, and (exclusive) freebies directly to your inbox.")

        return redirect("index")
