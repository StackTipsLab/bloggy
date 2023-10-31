from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import TemplateView
from hitcount.views import HitCountDetailView

from bloggy import settings
from bloggy.models import Post
from bloggy.models.course import Course

DEFAULT_PAGE_SIZE = 40


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="courses"), vary_on_cookie], name='dispatch')
class CoursesListView(TemplateView):
    model = Course
    template_name = "pages/archive/courses.html"
    paginate_by = DEFAULT_PAGE_SIZE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        courses = Course.objects.filter(publish_status="LIVE").order_by("-display_order")
        paginator = Paginator(courses, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context['courses'] = courses
        return context


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="course_single"), vary_on_cookie], name='dispatch')
class CourseDetailsView(HitCountDetailView):
    model = Course
    template_name = "pages/course_single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = self.object.meta_title
        context['meta_description'] = self.object.meta_description
        context['meta_keywords'] = self.object.meta_keywords
        if self.object.thumbnail:
            context['meta_image'] = self.object.thumbnail.url
        return context


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix="lesson_single"), vary_on_cookie], name='dispatch')
class LessonDetailsView(TemplateView):
    template_name = "pages/single/lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = context["course"]
        article = Post.objects.filter(course__slug=course_slug).filter(slug=context["slug"]).order_by("display_order").first()
        if not article:
            raise Http404

        context["article"] = article
        course = article.course
        context["course"] = course
        context['meta_title'] = article.meta_title
        context['meta_description'] = article.meta_description
        context['meta_keywords'] = article.meta_keywords
        if course.thumbnail:
            context['meta_image'] = course.thumbnail.url
        else:
            context['meta_image'] = f"{settings.ASSETS_DOMAIN}/media/opengraph/{article.post_type}/{article.slug}.png"
        return context
