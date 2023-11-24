import csv

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils.text import slugify

from bloggy.models import User


class Command(BaseCommand):
    help = 'Importing users'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content/users.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        counter = 0
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            print('Importing categories from file', file_path)

            for index, row in enumerate(reader):
                if index > 0:
                    counter = counter + 1

                    username = self.format_username(row[1])
                    try:
                        new_user = User.objects.create_user(
                            name=row[3],
                            password=make_password(row[0]),
                            username=username,
                            email=row[2])

                    except IntegrityError:
                        print("user exist")
                        new_user = User.objects.get(email=row[2])
                    finally:
                        print("user updating")

                    new_user.is_staff = row[4]
                    new_user.is_active = row[5]
                    new_user.website = row[6]
                    new_user.twitter = row[7]
                    new_user.linkedin = row[8]
                    new_user.youtube = row[9]
                    new_user.github = row[10]
                    new_user.bio = row[11]
                    new_user.save()
                    print("User updated {}", new_user)

        self.stdout.write(self.style.SUCCESS(f"Imported %s users" % counter))

    def format_username(self, username):
        formatted_username = slugify(username.replace(".", "_").lower())
        return formatted_username.replace("-", "_")
