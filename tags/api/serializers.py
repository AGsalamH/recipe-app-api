from rest_framework import serializers
from django.contrib.auth import get_user_model
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    '''Tag representation serializer.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'user')
        extra_kwargs = {
            'user': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = get_user_model().objects.get(id=data['user']).name
        return data
