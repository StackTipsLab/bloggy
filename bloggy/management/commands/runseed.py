from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importing demo contents'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--dir', type=str, help="File path to import, e.g. ~/bloggy/demo_content")

    def handle(self, *args, **options):
        file_path = options['dir']

        commands = [
            ('seed_users', 'users.csv'),
            ('seed_categories', 'categories.csv'),
            ('seed_posts', 'posts.csv'),
            ('seed_pages', 'pages.csv'),
            ('update_category_count', None),
        ]

        for command, file in commands:
            if file:
                call_command(command, f'--file={file_path}/{file}')
            else:
                call_command(command)

        self.stdout.write(self.style.SUCCESS("Import Complete!"))
