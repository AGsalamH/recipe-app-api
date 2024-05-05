'''
API Viewsets Router.
'''
from rest_framework.routers import DefaultRouter
from recipes.api.views import RecipeViewSet


router = DefaultRouter()

router.register('recipes', RecipeViewSet, 'recipe')


# app_name = 'api'
urlpatterns = router.urls
