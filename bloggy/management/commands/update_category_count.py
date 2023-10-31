from django.core.management.base import BaseCommand
from django.db import transaction

from bloggy.models import Category, Post


class Command(BaseCommand):
    help = 'Update Category Count'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        categories = Category.objects.select_for_update().all()
        with transaction.atomic():
            for category in categories:
                article_count = Post.objects.all().filter(category=category).count()
                if article_count > 0:
                    category.article_count = article_count
                category.save()

        self.stdout.write(self.style.SUCCESS('Updated category count.'))
