'''
Serializers for the User API Views.
'''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserRegisterationSerializer(serializers.ModelSerializer):
    '''Serializer for the user object'''
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            },
        }

    def create(self, validated_data):
        '''Create and return a user with encrypted password.'''
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    '''Serializer for the user Profile'''
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            },
            'email': {
                'read_only': True,
            },
        }

    def update(self, instance, validated_data):
        '''Update an existing user.'''
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
