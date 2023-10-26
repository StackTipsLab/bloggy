from rest_framework import generics

from bloggy.models import MyUser
from bloggy_api.serializers import UserSerializer


class UsersAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return MyUser.objects.filter(username=self.kwargs['username'])


