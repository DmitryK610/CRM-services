from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MaterialPurchaseViewSet


router = DefaultRouter()
router.register(r'material-purchases', MaterialPurchaseViewSet, basename='material-purchase')


urlpatterns = [
	path('', include(router.urls)),
]
