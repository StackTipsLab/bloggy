from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from bloggy.services.post_service import get_recent_quizzes, get_quiz_by_id
from bloggy_api.serializers import QuizSerializer


class QuizzesAPIView(generics.ListCreateAPIView):
    queryset = get_recent_quizzes()
    serializer_class = QuizSerializer


class QuizDetailsAPIView(APIView):

    def get_object(self, pk):
        return get_quiz_by_id(pk)

    def get(self, request, pk):
        quiz = self
        return Response(quiz.get_questions_json)
