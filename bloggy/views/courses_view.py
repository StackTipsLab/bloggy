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
from bloggy.services.post_service import set_seo_settings

DEFAULT_PAGE_SIZE = 40


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="courses"),
     vary_on_cookie],
    name='dispatch'
)
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


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="course_single"), vary_on_cookie],
    name='dispatch')
class CourseDetailsView(HitCountDetailView):
    model = Course
    template_name = "pages/single/course.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_seo_settings(post=self.object, context=context)
        context["posts"] = Post.objects.filter(course=self.object).order_by(
            "display_order").all()
        return context


@method_decorator(
    [cache_page(settings.CACHE_TTL, key_prefix="lesson_single"), vary_on_cookie],
    name='dispatch'
)
class LessonDetailsView(TemplateView):
    template_name = "pages/single/lesson.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guide_slug = context["course"]
        post = Post.objects.filter(course__slug=guide_slug).filter(slug=context["slug"]).order_by(
            "display_order").first()
        if not post:
            raise Http404

        context["post"] = post
        course = post.course
        context["course"] = course
        set_seo_settings(post=course, context=context)
        return context
