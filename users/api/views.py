'''
Views for the users API.
'''
from django.contrib.auth import get_user_model
from rest_framework import generics
from users.api.serializers import UserRegisterationSerializer


class CreateUserView(generics.CreateAPIView):
    '''Create a new user in the system.'''
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterationSerializer
