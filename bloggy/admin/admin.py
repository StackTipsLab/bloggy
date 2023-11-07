from django import forms
from django_summernote.admin import SummernoteModelAdmin

seo_fieldsets = ('SEO Settings', {
    'fields': ('meta_title', 'meta_description', 'meta_keywords'),
})

publication_fieldsets = ('Publication options', {
    'fields': ('publish_status', 'published_date',),
})


def publish(model_admin, request, queryset):
    queryset.update(publish_status='LIVE')


publish.short_description = "Publish"


def unpublish(model_admin, request, queryset):
    queryset.update(publish_status='DRAFT')


unpublish.short_description = "Unpublish"


class BloggyAdminForm(forms.ModelForm):
    excerpt = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 105}))
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 105}))
    meta_title = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 100}))
    meta_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))
    meta_keywords = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 100}))

    class Meta:
        abstract = True


class BloggyAdmin(SummernoteModelAdmin):
    actions = [publish, unpublish]
    list_per_page = 50

    def published_date_display(self, obj):
        return obj.published_date.strftime("%b %d, %Y")

    published_date_display.short_description = "Date Published"

    def author_display(self, obj):
        return '' + obj.author.name

    author_display.short_description = "Author"

    def is_published(self, queryset):
        if queryset.publish_status == 'LIVE':
            return True
        return False

    is_published.boolean = True

    class Meta:
        abstract = True
