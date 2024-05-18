'''
Recipe API serializers.
'''
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Recipe
from rest_framework.utils import model_meta

from tags.models import Tag
from tags.api.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    '''Recipe representation serializer.'''
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'description', 'link', 'price', 'user')
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = get_user_model().objects.get(id=data['user']).name
        return data


class TagRecipeSerializer(RecipeSerializer):
    '''Recipe with tags Serializer'''
    tags = TagSerializer(many=True, required=False)

    class Meta(RecipeSerializer.Meta):
        fields = list(RecipeSerializer.Meta.fields) + ['tags']

    def create(self, validated_data):
        tags = validated_data.pop('tags', None)
        recipe = Recipe.objects.create(**validated_data)

        # remove tags data from validated_data
        # Store tags in DB
        if tags:
            created_tags: list[Tag] = []
            auth_user = self.context['request'].user
            for tag in tags:
                # Get tag from db.
                # Create one if it does NOT exist.
                tag, _ = Tag.objects.get_or_create(
                    name=tag['name'],
                    user=auth_user
                )
                created_tags.append(tag)
            # Handle creating recipe logic
            recipe.tags.set(created_tags)
        recipe.save()

        return recipe

    def update(self, instance, validated_data):
        # get fields info
        info: model_meta.FieldInfo = model_meta.get_field_info(instance)

        # collect m2m fields
        many_to_many = {}
        for field, value in validated_data.items():
            # loop over fields and check if they represent a m2m relation.
            # if so, pop it from validated_data and append it to many_to_many
            if field in info.relations and info.relations[field].to_many:
                many_to_many[field] = value
            else:
                setattr(instance, field, value)

        instance.save()

        # Handling m2m fields
        for field, value in many_to_many.items():
            m2m_field = getattr(instance, field)
            for item in value:
                m2m_field.get_or_create(
                    **item,
                    user=instance.user  # auth_user
                )

        return instance
