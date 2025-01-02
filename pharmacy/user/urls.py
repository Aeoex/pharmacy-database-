from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, AdminProfileViewSet, register_user

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')
router.register(r'admin_profiles', AdminProfileViewSet, basename='adminprofile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register_user'),
]