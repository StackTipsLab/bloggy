import csv

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from bloggy.models import Category, Post, User


class Command(BaseCommand):
    help = 'Importing posts'

    def __init__(self, *args, **kwargs):
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str,
                            help="File path to import, e.g. ~/bloggy/demo_content/posts.csv")

    def handle(self, *args, **options):
        file_path = options['file']

        counter = 0
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            print('Importing articles from file', file_path)
            for index, row in enumerate(reader):
                if index > 0:
                    counter = counter + 1
                    slug = slugify(row[0])
                    article = Post.objects.get_or_create(
                        title=row[0],
                        slug=slug,
                        publish_status=row[1],
                        excerpt=row[2],
                        difficulty=row[3],
                        is_featured=row[4],
                        content=row[5],
                        video_id=row[8],
                        post_type=row[9],
                        template_type=row[10],
                        published_date=timezone.now(),
                        author=User.objects.get(id=row[7]),
                    )

                    categories = Category.objects.filter(slug__in=row[11].split(",")).all()
                    saved_article = Post.objects.get(slug=slug)
                    saved_article.category.set(categories)
                    saved_article.save()

        self.stdout.write(self.style.SUCCESS(f"Imported %s articles" % counter))
