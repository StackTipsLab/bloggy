import csv

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from bloggy.models import Category, RedirectRule


class Command(BaseCommand):
    help = 'Importing redirect rules'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content/redirect_rules.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        counter = 0
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            print('Importing redirect rules', file_path)

            for index, row in enumerate(reader):
                if index > 0:
                    counter = counter + 1
                    RedirectRule.objects.get_or_create(
                        from_url=row[0],
                        to_url=row[1],
                        status_code=row[2],
                        is_regx=row[3],
                        note=row[4]
                    )

        self.stdout.write(self.style.SUCCESS(f"%s redirect rules imported" % counter))
