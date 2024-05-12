'''
API Viewsets Router.
'''
from rest_framework.routers import DefaultRouter
from recipes.api.views import RecipeViewSet
from tags.api.views import TagViewSet


router = DefaultRouter()

router.register('recipes', RecipeViewSet, 'recipe')
router.register('tags', TagViewSet, 'tag')


# app_name = 'api'
urlpatterns = router.urls
