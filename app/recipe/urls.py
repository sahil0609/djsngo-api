from django.urls import path,include
from rest_framework.routers import DefaultRouter
from recipe.views import TagViewSet,ingredientsViewSet,recipeViewSet

router = DefaultRouter()
router.register('tags',TagViewSet)
router.register('ingredients',ingredientsViewSet)
router.register('recipe',recipeViewSet)

app_name='recipe'

urlpatterns = [
    path('',include(router.urls))
]
