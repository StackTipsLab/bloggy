from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from bloggy.admin.misc_admin import publish, unpublish
from bloggy.models.course import Course


class CourseForm(forms.ModelForm):
    excerpt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 105}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    meta_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 100}))
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    meta_keywords = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    model = Course


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'is_published', 'thumbnail_tag',
                    'display_order', 'author_display', 'published_date_display', 'display_order')
    list_filter = ('difficulty',
                   ("category", admin.RelatedOnlyFieldListFilter),
                   )

    fieldsets = (
        (None, {'fields': (
            'title',
            'excerpt',
            'slug',
            'description',
            'display_order',
            'thumbnail',
            'category',
            'difficulty',
            'is_featured')
        }),
        ('Publication options', {
            'fields': ('publish_status', 'published_date',),
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
        })
    )
    summernote_fields = ('description',)
    readonly_fields = ['thumbnail_tag']
    ordering = ('-display_order',)
    list_display_links = ['title']

    def published_date_display(self, obj):
        return obj.published_date.strftime("%b %d, %Y")

    published_date_display.short_description = "Date Published"

    def author_display(self, obj):
        return '' + obj.author.name

    author_display.short_description = "Author"

    form = CourseForm
    actions = [publish, unpublish]

    def is_published(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    is_published.boolean = True
