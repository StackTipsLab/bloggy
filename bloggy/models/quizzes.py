from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from hitcount.models import HitCount

from bloggy import settings
from bloggy.models import Category
from bloggy.models.mixin.Content import Content
from bloggy.models.mixin.updatable import Updatable
from bloggy.services.quiz_service import get_questions_json


def upload_thumbnail_image(self, post_id):
    return f'uploads/quizzes/{post_id}'


class Quiz(Content):
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advance', 'advance'),
        ],
        default='easy', blank=True, null=True,
        help_text="Select difficulty",
        verbose_name="Difficulty level")

    is_featured = models.BooleanField(
        default=False,
        help_text="Should this story be featured on site?"
    )
    content = TextField(
        null=True,
        help_text='Post content'
    )
    thumbnail = models.ImageField(
        upload_to=upload_thumbnail_image,
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        blank=True,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    duration = models.IntegerField(
        help_text="Duration in minutes. For articles, it will be calculated automatically.",
        default="1"
    )
    view_count = GenericRelation(
        HitCount,
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    @property
    def get_questions_json(self):
        return get_questions_json(self)

    def get_admin_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])

    def get_questions(self):
        return self.quizquestion_set.all()

    class Meta:
        ordering = ['title']
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        indexes = [
            models.Index(fields=['slug', 'publish_status']),
        ]


class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=500)
    description = TextField(
        null=True, blank=True,
        help_text='Enter description')
    explanation = TextField(
        null=True,
        blank=True,
        help_text='Enter explanation', )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    type = models.CharField(
        max_length=20,
        choices=[
            ('binary', 'binary'),
            ('multiple', 'multiple'),
        ],
        default='binary', blank=True, null=True,
        help_text="Select type of question",
        verbose_name="Question type")

    def __str__(self):
        return self.title

    def get_answers(self):
        return self.quizanswer_set.all()


class QuizAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.title}, answer: {self.content}, correct: {self.correct}"


class UserQuizScore(Updatable):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)
