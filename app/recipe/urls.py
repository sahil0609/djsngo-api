from django.urls import path,include
from rest_framework.routers import DefaultRouter
from recipe.views import TagViewSet,ingredientsViewSet

router = DefaultRouter()
router.register('tags',TagViewSet)
router.register('ingredients',ingredientsViewSet)

app_name='recipe'

urlpatterns = [
    path('',include(router.urls))
]
