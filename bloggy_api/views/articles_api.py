from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from bloggy.models import Post
from bloggy_api.serializers import ArticleSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'


class ArticleAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(publish_status="LIVE") \
            .order_by("-published_date")

        categories = self.request.query_params.getlist('category', None)
        if categories and len(categories) > 0:
            queryset = queryset.filter(category__slug__in=categories)

        post_type = self.request.query_params.getlist('post_type', None)
        if post_type and len(post_type) > 0:
            queryset = queryset.filter(post_type__in=post_type)

        return queryset


class ArticleDetailsAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Post.objects.filter(publish_status="LIVE").all()
    lookup_field = 'slug'
