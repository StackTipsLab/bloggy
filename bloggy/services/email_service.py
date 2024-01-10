from django.core.mail import send_mail
from django.template.loader import render_to_string

from bloggy import settings


def send_html_email(subject, to_email, template, args, from_email=settings.DEFAULT_FROM_EMAIL):
    email_body = render_to_string(template, args)
    send_mail(
        subject,
        email_body,
        from_email,
        to_email,
        fail_silently=False,
        html_message=email_body
    )


def send_plain_email(subject, to_email, message_content, from_email=settings.DEFAULT_FROM_EMAIL):
    send_mail(
        subject,
        message_content,
        from_email,
        to_email,
        fail_silently=False,
    )

# def email_verification_token(request, new_user, token):
#     subject = f"{settings.SITE_TITLE} confirmation code: {token.code}"
#     args = {
#         "email_subject": subject,
#         "verification_code": token.code,
#         "app_name": settings.SITE_TITLE,
#         "verification_link": request.build_absolute_uri(reverse("otp_verification", args=[token.uuid]))
#     }
#     send_html_email(subject, [new_user.email], "email/login_code_email.html", args)
