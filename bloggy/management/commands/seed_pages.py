import csv

from django.core.management.base import BaseCommand
from bloggy.models.page import Page


class Command(BaseCommand):
    help = 'Importing pages'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content/pages.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        counter = 0
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            print('Importing pages from file', file_path)
            for index, row in enumerate(reader):
                if index > 0:
                    counter = counter + 1
                    Page.objects.get_or_create(
                        title=row[0],
                        url=row[1],
                        publish_status=row[2],
                        meta_title=row[3],
                        meta_description=row[4],
                        meta_keywords=row[5],
                        excerpt=row[6],
                        content=row[7],
                    )

        self.stdout.write(self.style.SUCCESS(f"Imported %s pages" % counter))
