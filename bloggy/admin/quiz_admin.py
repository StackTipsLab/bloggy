from django import forms
from django.contrib import admin
from django.utils.html import format_html

from bloggy.admin import BloggyAdminForm, BloggyAdmin, publication_fieldsets, seo_fieldsets
from bloggy.models.quizzes import QuizAnswer, QuizQuestion, Quiz, UserQuizScore


class QuizForm(BloggyAdminForm):
    model = Quiz


@admin.register(Quiz)
class QuizAdmin(BloggyAdmin):
    prepopulated_fields = {
        "slug": ("title",)
    }
    list_display = (
        'id',
        'title',
        'category',
        'is_published',
        'display_order',
        'published_date_display')

    list_filter = (
        'publish_status',
        ("category", admin.RelatedOnlyFieldListFilter),
    )

    fieldsets = (
        (None, {
            'fields': (
                'title', 'excerpt', 'slug', 'content', 'thumbnail', 'category', 'difficulty', 'is_featured', 'duration')
        }),
        publication_fieldsets, seo_fieldsets)

    summernote_fields = ('content',)
    readonly_fields = ['thumbnail_tag']
    ordering = ('-display_order',)
    list_display_links = ['title']
    form = QuizForm


    def thumbnail_tag(self):
        if self.thumbnail:
            return format_html(f'<img src="{self.thumbnail.url}" width="auto" height="40"/>')
        return ""

    thumbnail_tag.short_description = 'Logo'
    thumbnail_tag.allow_tags = True


class QuizAnswerInLine(admin.TabularInline):
    model = QuizAnswer


class QuizQuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 105}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 105}))
    explanation = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 105}))
    type = forms.Select()
    model = QuizQuestion


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    inlines = [QuizAnswerInLine]
    list_display = ('title', 'type')
    form = QuizQuestionForm
    list_filter = [
        "type",
        ("quiz", admin.RelatedOnlyFieldListFilter)
    ]


@admin.register(QuizAnswer)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'correct', 'display_question_id', 'display_question_title')
    list_filter = [
        ("question", admin.RelatedOnlyFieldListFilter)
    ]

    def display_question_id(self, obj):
        return obj.question.id

    display_question_id.short_description = "Question id"

    def display_question_title(self, obj):
        return obj.question.title

    display_question_title.short_description = "Question"


@admin.register(UserQuizScore)
class UserQuizScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'display_quiz_id', 'user', 'score')
    readonly_fields = ['score']
    list_display_links = ['quiz']
    actions = None
    list_filter = [
        ("user", admin.RelatedOnlyFieldListFilter),
        ("quiz", admin.RelatedOnlyFieldListFilter)
    ]

    def display_quiz_id(self, obj):
        return obj.quiz.id

    display_quiz_id.short_description = "Quiz ID"
