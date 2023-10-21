from django_summernote.admin import SummernoteModelAdmin

from django.contrib import admin
from bloggy.models.comment import Comment


def approve_comments(request, queryset):
    queryset.update(active=True)


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = (
        'comment_content',
        'comment_author_name',
        'comment_author_email',
        'comment_author_url',
        'comment_author_ip',
        'post',
        'comment_date',
        'active')
    list_filter = ('active', 'comment_date')
    search_fields = ('user', 'user', 'comment_content')
    actions = ['approve_comments']