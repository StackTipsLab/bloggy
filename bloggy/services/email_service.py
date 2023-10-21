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
    subject = "Confirm to StackTips newsletter"

    args = {
        "email_subject": subject,
        "app_name": settings.SITE_TITLE,
        "verification_link": request.build_absolute_uri(reverse("newsletter_verification", args=[uuid, token]))
    }

    send_custom_email(subject, [email], "email/newsletter_verification_token.html", args)


def email_verification_token(request, new_user, token):
    subject = "{} confirmation code: {}".format(settings.SITE_TITLE, token.code)
    args = {
        "email_subject": subject,
        "verification_code": token.code,
        "app_name": settings.SITE_TITLE,
        "verification_link": request.build_absolute_uri(reverse("otp_verification", args=[token.uuid]))
    }
    send_custom_email(subject, [new_user.email], "email/login_code_email.html", args)


def email_registration_token(request, new_user, verification_token):
    subject = "Welcome to StackTips! Complete your registration and get started!"
    args = {
        "email_subject": subject,
        "user_name": new_user.name,
        "app_name": settings.SITE_TITLE,
        "verification_link": request.build_absolute_uri(reverse("activate_account", args=[
            verification_token.uuid,
            verification_token.token
        ]))
    }

    send_custom_email(subject, [new_user.email], "email/acc_active_email.html", args)
