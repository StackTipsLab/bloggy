from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from bloggy import settings


def send_custom_email(subject, recipients, template, args, from_email=settings.DEFAULT_FROM_EMAIL):
    email_body = render_to_string(template, args)
    send_mail(
        subject,
        email_body,
        from_email,
        recipients,
        fail_silently=False,
        html_message=email_body
    )


def send_newsletter_verification_token(request, email, uuid, token):
    subject = f'Confirm to {settings.SITE_TITLE} newsletter'

    args = {
        "email_subject": subject,
        "app_name": settings.SITE_TITLE,
        "verification_link": request.build_absolute_uri(reverse("newsletter_verification", args=[uuid, token]))
    }

    send_custom_email(subject, [email], "email/newsletter_verification_token.html", args)


def email_verification_token(request, new_user, token):
    subject = f"{settings.SITE_TITLE} confirmation code: {token.code}"
    args = {
        "email_subject": subject,
        "verification_code": token.code,
        "app_name": settings.SITE_TITLE,
        "verification_link": request.build_absolute_uri(reverse("otp_verification", args=[token.uuid]))
    }
    send_custom_email(subject, [new_user.email], "email/login_code_email.html", args)


def send_account_activation_email(request, new_user, verification_token):
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

    send_custom_email(subject, [new_user.email], "email/account_activation_email.html", args)