from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from advertisements.views import AdvertisementViewSet, FavoriteViewSet, RegisterView

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet, basename='advertisement')
router.register('favorites', FavoriteViewSet, basename='favourite')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view()),
]
