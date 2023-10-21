import json

from django.contrib import auth
from django.http import HttpResponse
from rest_framework.views import APIView

from bloggy.models import Article
from bloggy.models.quizzes import UserQuizScore
from bloggy_api.exception.unauthorized_access import UnauthorizedAccess


class SaveUserScore(APIView):
    model = UserQuizScore

    def post(self, request):
        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()

        json_body = request.data
        quiz_id = json_body.get('quiz_id')
        score = json_body.get('score')
        user = auth.get_user(request)

        UserQuizScore.objects.create(quiz=Article.objects.get(id=quiz_id), user=user, score=score)
        return HttpResponse(json.dumps({"result": "created", }), content_type="application/json")
