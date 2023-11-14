from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from bloggy import settings
from bloggy.models.quizzes import Quiz
from bloggy.services.post_service import DEFAULT_PAGE_SIZE, get_recent_quizzes, set_seo_settings


@method_decorator([
    cache_page(settings.CACHE_TTL, key_prefix="quizzes"),
    vary_on_cookie],
    name='dispatch'
)
class QuizListView(ListView):
    model = Quiz
    template_name = "pages/archive/quizzes.html"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        context['quizzes'] = get_recent_quizzes()
        return context


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="quiz_single"), vary_on_cookie],
    name='dispatch'
)
class QuizDetailView(HitCountDetailView):
    model = Quiz
    template_name = "pages/single/quiz.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_seo_settings(post=self.object, context=context)
        return context
