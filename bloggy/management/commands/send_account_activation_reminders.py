from django.core.management.base import BaseCommand
from django.urls import reverse

from bloggy import settings
from bloggy.services import email_service
from bloggy.services.token_service import create_token
from bloggy.models import User


class Command(BaseCommand):
    help = 'Send email reminders to users who have not activated their accounts'

    def handle(self, *args, **kwargs):
        # Get a list of users who have not activated their accounts
        inactive_users = User.objects.filter(is_active=False)

        email_count = 0
        for user in inactive_users:
            subject = 'Reminder: Verify your email to activate your account'

            verification_token = create_token(user=user, token_type="signup")
            verification_link = reverse("activate_account", args=[
                verification_token.uuid,
                verification_token.token
            ])

            args = {
                "email_subject": subject,
                "app_name": settings.SITE_TITLE,
                "verification_link": settings.SITE_URL + verification_link
            }

            try:
                email_service.send_html_email(
                    subject,
                    [user.email],
                    "email/account_activation_reminder_email.html",
                    args)
                print('Success: Account activation reminder mail sent to {}', user.email)

            except Exception as ex:
                print('Error: sending email to {}: {}', user.email, ex)

            finally:
                email_count = email_count + 1

            self.stdout.write(self.style.SUCCESS(f"Reminder sent to {email_count} users"))
