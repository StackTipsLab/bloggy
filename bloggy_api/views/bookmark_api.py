import json
from django.contrib import auth
from django.http import HttpResponse
from rest_framework.views import APIView

from bloggy.models import Bookmarks
from bloggy_api.exception.unauthorized_access import UnauthorizedAccess


class BookmarkAPIView(APIView):
    model = Bookmarks

    def get(self, request):
        post_id = self.request.query_params.get('post_id', None)
        post_type = self.request.query_params.get('post_type', None)

        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()

        if post_id is None or post_type is None:
            return HttpResponse(
                status=400,
                content=json.dumps({
                    "errorCode": "BAD_REQUEST",
                    "message": "post_id or post_type is missing"
                }),
                content_type="application/json"
            )

        return HttpResponse(
            status=200,
            content=json.dumps({
                "userBookmarkCount": self.model.objects.filter(user=user, post_id=post_id, post_type=post_type).count(),
                # "totalBookmarks": self.model.objects.filter(post_id=post_id, post_type=post_type).count()
            }),
            content_type="application/json"
        )

    def post(self, request):
        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()
        json_body = request.data
        post_id = json_body.get('post_id')
        post_type = json_body.get('post_type')

        # Trying to get a bookmark from the table, or create a new one
        bookmark, created = Bookmarks.objects.get_or_create(user=user, post_id=post_id, post_type=post_type)

        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                # "result": created,
                "userBookmarkCount": Bookmarks.objects.filter(user=user, post_id=post_id, post_type=post_type).count(),
                # "totalBookmarks": self.model.objects.filter(post_id=post_id, post_type=post_type).count()
            }),

            content_type="application/json"
        )
