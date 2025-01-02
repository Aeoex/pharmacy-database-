from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PharmacyViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'pharmacies', PharmacyViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
