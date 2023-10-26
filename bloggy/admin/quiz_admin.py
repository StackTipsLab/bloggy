from django import forms
from django.contrib import admin

from bloggy.models import Article
from bloggy.models.quizzes import QuizAnswer, QuizQuestion, UserQuizScore


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

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["article"].queryset = Article.objects.filter(post_type__exact="quiz")
        return form

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

    display_question_id.short_description = "Question ID"

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
