import csv

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from bloggy.models import Category


class Command(BaseCommand):
    help = 'Importing Categories from CSV'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/management/commands/demo/categories.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        with open(file_path) as f:
            reader = csv.reader(f)
            print('Importing categories from file', file_path)

            for index, row in enumerate(reader):
                if index > 0:
                    Category.objects.get_or_create(
                        title=row[0],
                        slug=slugify(row[1]),
                        description=row[2],
                        logo=row[3],
                        color=row[4],
                        publish_status=row[5]

                    )
        self.stdout.write(self.style.SUCCESS(f'Imported ' + str(index - 1) + ' categories'))
