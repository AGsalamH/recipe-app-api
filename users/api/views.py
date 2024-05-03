'''
Views for the users API.
'''
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import (
    UserRegisterationSerializer,
    UserProfileSerializer
)


class CreateUserView(generics.CreateAPIView):
    '''Create a new user in the system.'''
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterationSerializer


class RetrieveUpdateProfileView(generics.RetrieveUpdateAPIView):
    '''Retrieve and modify profile data for a user.'''
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
