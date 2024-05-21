'''
Recipe API views.
'''
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe
from recipes.api.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    '''Recipes model CRUD viewset.'''
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user.id
        ).select_related('user').prefetch_related('tags', 'ingredients')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
