from django.core.management.base import BaseCommand
from bloggy import settings
from bloggy.models.subscriber import Subscribers
from bloggy.services import email_service
from bloggy.models import User
from itertools import chain


# python3 manage.py send_card --cardImgUrl="https://media.stacktips.com/media/emails/christmas-card.gif" --subject="Merry Christmas." --targetLink="https://stacktips.com"
class Command(BaseCommand):
    help = 'Send wish card to users'

    def add_arguments(self, parser):
        parser.add_argument('--cardImgUrl', type=str, required=True, help='URL of the card')
        parser.add_argument('--subject', type=str, required=True, help='Email subject')
        parser.add_argument('--targetLink', type=str, required=True, help='Target link')

    def handle(self, *args, **options):
        card_img_url = options['cardImgUrl']
        subject = options['subject']
        target_link = options['targetLink']

        if card_img_url is None or target_link is None or subject is None:
            self.stdout.write(
                self.style.ERROR(f"Missing mandatory arguments --cardImgUrl or --subject or --targetLink"))

        else:
            users = chain(
                User.objects.all(),
                Subscribers.objects.all(),
            )

            email_count = 0
            for user in users:
                args = {
                    "user_name": user.name,
                    "email_subject": subject,
                    "app_name": settings.SITE_TITLE,
                    "card_img_url": card_img_url,
                    "card_target_link": target_link
                }

                try:
                    email_service.send_custom_email(subject, [user.email], "email/wish_card_email.html", args)
                    print('Success: Card sent to {}', user.email)
                except Exception as ex:
                    print('Error sending card to {}: {}', user.email, ex)
                finally:
                    email_count = email_count + 1

                self.stdout.write(self.style.SUCCESS(f"Reminder sent to {email_count} users"))
