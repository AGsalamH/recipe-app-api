from rest_framework import serializers
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    '''Ingredient representation.'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'user')
        read_only_fields = ('user',)

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user  # auth_user
        return super().save(**kwargs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        auth_user = get_user_model().objects.get(id=data['user'])
        data['user'] = auth_user.name
        return data
