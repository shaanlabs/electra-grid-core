from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChargingStationViewSet, ChargingSessionViewSet, ReviewViewSet, FavoriteStationViewSet

router = DefaultRouter()
router.register(r'stations', ChargingStationViewSet)
router.register(r'sessions', ChargingSessionViewSet, basename='session')
router.register(r'reviews', ReviewViewSet)
router.register(r'favorites', FavoriteStationViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
] 