'''
Serializers for the User API Views.
'''
from rest_framework import serializers
from django.contrib.auth import get_user_model


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

    def update(self, instance, validated_data):
        '''Update an existing user.'''
        password = validated_data.pop('password')
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
