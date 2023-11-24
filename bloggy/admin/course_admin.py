from django.contrib import admin
from bloggy.admin import BloggyAdmin, BloggyAdminForm, seo_fieldsets, publication_fieldsets
from bloggy.models.course import Course


class CourseForm(BloggyAdminForm):
    model = Course


@admin.register(Course)
class CourseAdmin(BloggyAdmin):
    prepopulated_fields = {
        "slug": ("title",)
    }
    list_display = (
        'id',
        'title',
        'is_published',
        'thumbnail_tag',
        'display_order',
        'author_display',
        'published_date_display',
        'display_order')

    list_filter = (
        'difficulty',
        ("category", admin.RelatedOnlyFieldListFilter),
    )

    fieldsets = ((None, {'fields': (
        'title',
        'excerpt',
        'slug',
        'description',
        'display_order',
        'thumbnail',
        'category',
        'difficulty',
        'is_featured')
    }), publication_fieldsets, seo_fieldsets)

    summernote_fields = ('description',)
    readonly_fields = ['thumbnail_tag']
    ordering = ('-display_order',)
    list_display_links = ['title']
    form = CourseForm



