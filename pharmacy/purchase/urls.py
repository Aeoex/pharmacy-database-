from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'purchases', views.PurchaseViewSet, basename='purchase')
router.register(r'purchase-items', views.PurchaseItemViewSet, basename='purchase-item')

urlpatterns = [
    path('cart/add/<int:drug_id>/<int:pharmacy_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('cart/view/', views.view_cart, name='view_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/checkout/', views.checkout_cart, name='checkout_cart'),
]

urlpatterns += router.urls  # Add the router-generated URLs to the existing ones