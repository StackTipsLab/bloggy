from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importing demo_content contents'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content")

    def handle(self, *args, **options):
        file_path = options['path']
        print('Importing demo_content contents')

        call_command('import_categories', f'--file={file_path}/categories.csv')
        call_command('import_articles', f'--file={file_path}/posts.csv')
        call_command('import_pages', f'--file={file_path}/pages.csv')
        call_command('update_category_count')

        self.stdout.write(self.style.SUCCESS("Import Complete!"))
