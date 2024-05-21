from rest_framework import serializers

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
        data['user'] = self.context['request'].user.name  # auth_user
        return data
