from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DrugViewSet

# Create a router and register the DrugViewSet
router = DefaultRouter()
router.register(r'drug', DrugViewSet, basename='drug')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
