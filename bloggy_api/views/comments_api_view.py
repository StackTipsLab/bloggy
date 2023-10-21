from django.contrib import auth
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from bloggy.models import Comment
from bloggy_api.serializers import CommentSerializer
from bloggy_api.exception.not_found_exception import NotFoundException
from bloggy_api.exception.unauthorized_access import UnauthorizedAccess


class CommentsAPIView(APIView):
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()

        json_body = request.data
        comment = Comment.objects.create(
            post_id=json_body.get('postId'),
            comment_content=json_body.get('comment'),
            parent_id=json_body.get('parent'),
            user=user,
            active=False
        )

        serializer = CommentSerializer(comment, many=False)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        comments_data = Comment.objects.prefetch_related('reply_set').filter(post_id=kwargs['id']).order_by(
            "-comment_date").all()

        serializer = CommentSerializer(comments_data, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if user.is_anonymous:
            raise UnauthorizedAccess()

        try:
            comment = Comment.objects.get(id=kwargs['id'])
            if comment and user.id == comment.user_id:
                comment.delete()
                return HttpResponse(status=204)

        except Comment.DoesNotExist:
            raise NotFoundException(default_detail="Comment with id {} doesn't exist".format(kwargs['id']));

    @staticmethod
    def find_children(comment_id, comments):
        return list(filter(lambda comment: comment['parent'] == comment_id, comments))
