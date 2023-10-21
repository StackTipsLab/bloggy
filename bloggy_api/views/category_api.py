from rest_framework import generics

from bloggy.models import Category
from bloggy_api.serializers import CategorySerializer


class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(article_count__gt=0).order_by("-article_count").all()
    serializer_class = CategorySerializer
