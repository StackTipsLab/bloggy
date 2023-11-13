from django import forms
from django.contrib import admin
from django.utils.html import format_html

from bloggy.admin import seo_fieldsets
from bloggy.admin.admin import publish, unpublish
from bloggy.models import Category


class CategoryForm(forms.ModelForm):
    excerpt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 105}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    slug = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    meta_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 100}))
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    meta_keywords = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    model = Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'is_category_published',
        'thumbnail_tag',
        'article_count',
        'slug',
        'display_updated_date',
        'display_color',
    )

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'thumbnail', 'color', 'publish_status')
        }),
        seo_fieldsets
    )

    show_change_link = True
    form = CategoryForm
    readonly_fields = ['thumbnail_tag', 'article_count']
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 50
    ordering = ('-article_count',)
    list_filter = ['publish_status']
    search_fields = ['title', 'slug']
    actions = [publish, unpublish]

    def is_category_published(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    is_category_published.boolean = True

    def display_updated_date(self, obj):
        return obj.updated_date.strftime("%m/%d/%Y") if obj.updated_date else "-"

    display_updated_date.short_description = "Published on"

    def display_color(self, obj):
        return format_html(f'<div style="background:{obj.color};width:30px;height:20px;"></div>')

    display_color.short_description = "Color"
