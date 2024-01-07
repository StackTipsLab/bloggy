from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from bloggy.admin import BloggyAdmin, BloggyAdminForm, publication_fieldsets, seo_fieldsets
from bloggy.models import Post
from bloggy.services.post_service import cleanse_html


class PostForm(BloggyAdminForm):
    model = Post


@admin.register(Post)
class PostAdmin(BloggyAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    summernote_fields = ('content',)
    readonly_fields = ['updated_date', 'created_date']
    date_hierarchy = 'published_date'
    form = PostForm
    ordering = ('-created_date',)
    list_display_links = ['title']
    list_display = (
        'id',
        'title',
        'category_display',
        'post_type',
        'template_type',
        'is_published',
        'author_link',
        'display_order',
        'published_date_display',
        'updated_date_display'
    )
    list_filter = (
        'publish_status',
        ('post_type', admin.ChoicesFieldListFilter),
        ('template_type', admin.ChoicesFieldListFilter),
        ("category", admin.RelatedOnlyFieldListFilter),
        ("author", admin.RelatedOnlyFieldListFilter),
        ("course", admin.RelatedOnlyFieldListFilter),
        'is_featured',
        ("video_id", admin.BooleanFieldListFilter),
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'excerpt', 'slug', 'content', 'thumbnail', 'author', 'category',)
        }),
        publication_fieldsets,
        ('Advanced options', {
            'fields': ('post_type', 'template_type', 'course', 'difficulty', 'video_id', 'github_link', 'is_featured',
                       'display_order'),
        }),
        seo_fieldsets)

    def get_changeform_initial_data(self, request):
        return {
            'meta_title': '{title}',
            'meta_description': '{excerpt}'
        }

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["author"].queryset = get_user_model().objects.filter(is_staff=True)
        return form

    def updated_date_display(self, obj):
        return format_html(
            f'<small>{obj.updated_date.strftime("%m/%d/%Y") if obj.published_date else "-"}</small>')

    updated_date_display.short_description = "Updated on"

    def category_display(self, obj):
        tags = "</br>".join([
            "<span class='tags-list'>" + cat.title + "</span></br>" for cat in obj.category.all()
        ])
        return format_html(tags)

    category_display.short_description = "Categories"

    def author_link(self, obj):
        url = reverse("admin:bloggy_user_change", args=[obj.author.id])
        if obj.author.name:
            link = f'<a href="{url}">{obj.author.name}</a>'
        else:
            link = f'<a href="{url}">{obj.author.username}</a>'
        return mark_safe(link)

    author_link.short_description = 'Author'

    def view_on_site(self, obj):
        url = reverse('post_single', kwargs={'slug': obj.slug})
        return url + "?context=preview"

    def save_model(self, request, obj, form, change):
        if "publish_status" in form.changed_data and obj.publish_status == "LIVE" and not obj.published_date:
            obj.published_date = timezone.now()
        if not obj.pk:
            obj.author = request.user
        obj.content = cleanse_html(obj.content)

        super().save_model(request, obj, form, change)

    def live_category(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    def has_excerpt(self, queryset):
        if queryset.excerpt is None:
            return False
        return True

    has_excerpt.boolean = True
