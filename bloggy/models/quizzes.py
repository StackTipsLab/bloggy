from django.db import models
from django.db.models import TextField

from bloggy.models import MyUser, Article
from bloggy.models.updatable import Updatable


def upload_logo_image(self, filename):
    return f'uploads/quiz/{filename}'


QUESTION_TYPE = [
    ('binary', 'binary'),
    ('multiple', 'multiple'),
]


class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = TextField(null=True, blank=True, help_text='Enter description')
    explanation = TextField(null=True, blank=True, help_text='Enter explanation', )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(
        max_length=20, choices=QUESTION_TYPE,
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
    quiz = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.quiz)
