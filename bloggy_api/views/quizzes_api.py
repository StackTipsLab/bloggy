from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from bloggy.models import Quiz
from bloggy.services.post_service import get_recent_quizzes
from bloggy_api.serializers import QuizSerializer


class QuizzesAPIView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return get_recent_quizzes()


class QuizDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        quiz = self
        return Response(quiz.get_questions_json)
