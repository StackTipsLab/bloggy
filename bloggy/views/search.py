from itertools import chain

from django.views.generic import ListView

from bloggy.models import Category, Post
from bloggy.utils.string_utils import StringUtils

DEFAULT_PAGE_SIZE = 30


class SearchListView(ListView):
    model = Post
    template_name = "pages/search_result.html"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get("q")
        context = super().get_context_data(**kwargs)

        if StringUtils.is_not_blank(search_query):
            categories = Category.objects.filter(slug__icontains=search_query)[:5]
            results = chain(
                Post.objects.filter(title__icontains=search_query, excerpt__icontains=search_query, publish_status="LIVE"),
            )

            context['posts'] = results
            context['categories'] = categories
            context['search_query'] = search_query
            context['meta_title'] = f"Search result for {search_query}"
            context['meta_description'] = "Search articles"

        return context
