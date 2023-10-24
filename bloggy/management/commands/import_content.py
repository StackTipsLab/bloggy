from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Importing demo contents'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str,
                            help="File path to import, e.g. ~/bloggy/management/commands/demo")

    def handle(self, *args, **options):
        file_path = options['path']
        print('Importing demo contents')

        call_command('import_categories', '--file={}/categories.csv'.format(file_path))
        self.stdout.write(self.style.SUCCESS("Import Complete!"))
