from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import TextField
from django.forms import Textarea, BaseInlineFormSet
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from bloggy.admin.misc_admin import publish, unpublish
from bloggy.models import Article, PostMeta


class ArticleForm(forms.ModelForm):
    excerpt = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    model = Article
    keywords = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))


class PostMetaInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.initial = [
            {'meta_key': 'template_type', 'meta_value': "standard"},
            {'meta_key': 'seo_title', 'meta_value': ""},
            {'meta_key': 'seo_description', 'meta_value': ""},
            {'meta_key': 'seo_keywords', 'meta_value': ""},
        ]
        # super(PostMetaInlineFormSet, self).__init__(*args, **kwargs)
        super().__init__()


class PostMetaInline(admin.TabularInline):
    model = PostMeta
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 105})},
    }
    formset = PostMetaInlineFormSet


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["author"].queryset = get_user_model().objects.filter(is_staff=True)
        return form

    prepopulated_fields = {"slug": ("title",)}
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
            'fields': ('title', 'excerpt', 'keywords', 'slug', 'content', 'thumbnail', 'author', 'category',)
        }),
        ('Publication options', {
            'fields': ('publish_status', 'published_date',),
        }),
        ('Advanced options', {
            'fields': ('post_type', 'template_type', 'course', 'duration', 'difficulty', 'video_id', 'is_featured',
                       'display_order'),
        }),
    )

    search_fields = ['title']
    summernote_fields = ('content',)
    readonly_fields = ['updated_date', 'created_date']
    date_hierarchy = 'published_date'
    form = ArticleForm
    ordering = ('-created_date',)
    list_display_links = ['title']
    list_per_page = 50
    actions = [publish, unpublish]
    inlines = [PostMetaInline]

    def published_date_display(self, obj):
        return format_html(
            '<small>{}</small>'.format(obj.published_date.strftime("%m/%d/%Y") if obj.published_date else "-"))

    published_date_display.short_description = "Published on"

    def has_video(self):
        return self.video_id

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
        url = reverse("admin:bloggy_myuser_change", args=[obj.author.id])
        if obj.author.name:
            link = f'<a href="{url}">{obj.author.name}</a>'
        else:
            link = f'<a href="{url}">{obj.author.username}</a>'
        return mark_safe(link)

    author_link.short_description = 'Author'

    def view_on_site(self, obj):
        url = reverse('article_single', kwargs={'slug': obj.slug})
        return url + "?context=preview"

    def save_model(self, request, obj, form, change):
        if "publish_status" in form.changed_data and obj.publish_status == "LIVE" and not obj.published_date:
            obj.published_date = timezone.now()
        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)

    def live_category(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    def is_published(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    is_published.boolean = True
    is_published.short_description = "Status"

    def has_excerpt(self, queryset):
        if queryset.excerpt is None:
            return False
        return True

    has_excerpt.boolean = True


@admin.register(PostMeta)
class PostMetaAdmin(admin.ModelAdmin):
    list_display = ['id', 'article_link', 'meta_key', 'meta_value']
    list_filter = ['meta_key']

    def article_link(self, obj):
        url = reverse("admin:bloggy_article_change", args=[obj.article.id])
        link = f'<a href="{url}">{obj.article.title}</a>'
        return mark_safe(link)

    article_link.short_description = 'Author'
