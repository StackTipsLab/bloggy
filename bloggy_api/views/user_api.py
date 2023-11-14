from rest_framework import generics

from bloggy.models import User
from bloggy_api.serializers import UserSerializer


class UsersAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])
