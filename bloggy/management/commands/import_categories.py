import csv

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from bloggy.models import Category


class Command(BaseCommand):
    help = 'Importing Categories'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content/categories.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        counter = 0
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            print('Importing categories from file', file_path)

            for index, row in enumerate(reader):
                if index > 0:
                    counter = counter + 1
                    Category.objects.get_or_create(
                        title=row[0],
                        slug=slugify(row[1]),
                        description=row[2],
                        logo=row[3],
                        color=row[4],
                        publish_status=row[5]
                    )

        self.stdout.write(self.style.SUCCESS(f"Imported %s categories" % counter))
