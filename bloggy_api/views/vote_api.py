import json

from django.contrib import auth
from django.http import HttpResponse
from rest_framework.views import APIView

from bloggy.models import Votes
from bloggy_api.exception.unauthorized_access import UnauthorizedAccess


class VoteAPIView(APIView):
    model = Votes

    def post(self, request):

        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()

        json_body = request.data
        post_id = json_body.get('post_id')
        post_type = json_body.get('post_type')

        vote, created = Votes.objects.get_or_create(
            user=user, post_id=post_id, post_type=post_type)
        if not created:
            vote.delete()

        return HttpResponse(json.dumps({
            "result": created,
            "userVoteCount": Votes.objects.filter(user=user, post_id=post_id, post_type=post_type).count(),
            "count": self.model.objects.filter(post_id=post_id, post_type=post_type).count()
        }), content_type="application/json")
