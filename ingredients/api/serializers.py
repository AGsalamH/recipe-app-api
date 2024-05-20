from rest_framework import serializers

from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    '''Ingredient representation.'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name')

    def save(self, **kwargs):
        kwargs['user'] = self.context['request'].user  # auth_user
        return super().save(**kwargs)
