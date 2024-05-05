'''
Recipe API serializers.
'''
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    '''Recipe representation serializer.'''
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'description', 'link', 'price', 'user')


    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['user'] = get_user_model().objects.get(id=data['user']).name
        return data
