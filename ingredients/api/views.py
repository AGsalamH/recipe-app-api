from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ingredients.models import Ingredient
from ingredients.api.serializers import IngredientSerializer


class IngredientviewSet(ModelViewSet):
    queryset = Ingredient.objects.select_related('user').order_by('-name')
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)
