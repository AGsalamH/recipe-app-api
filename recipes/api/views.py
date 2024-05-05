'''
Recipe API views.
'''
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.models import Recipe
from recipes.api.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    '''Recipes model CRUD viewset.'''
    queryset = Recipe.objects.select_related('user').all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
