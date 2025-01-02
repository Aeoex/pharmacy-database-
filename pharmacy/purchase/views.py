from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes 
from .models import Purchase, PurchaseItem
from .serializers import PurchaseSerializer, PurchaseItemSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from drug.models import Drug
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt


def deduct_stock(drug, quantity):
    if quantity > drug.quantity:
        raise ValidationError({"error": f"Not enough stock available for {drug.name}. Only {drug.quantity} available."})
    drug.quantity -= quantity
    drug.save()

def add_to_cart(request, drug_id, pharmacy_id, quantity):
    """
    Add a drug to the session cart.
    """
    drug = get_object_or_404(Drug, id=drug_id)
    
    if drug.quantity < quantity:
        raise ValidationError({"error": f"Not enough stock for {drug.name}. Only {drug.quantity} available."})
    
    cart = request.session.get('cart', {})
    key = f"{pharmacy_id}_{drug_id}"
    cart[key] = cart.get(key, 0) + quantity
    request.session['cart'] = cart
    request.session.modified = True
    
    return JsonResponse({"message": f"{drug.name} added to cart", "cart": cart})


def view_cart(request):
    """
    Retrieve the cart from the session.
    """
    cart = request.session.get('cart', {})
    return JsonResponse({"cart": cart})

def clear_cart(request):
    """
    Clear the cart from the session.
    """
    request.session.pop('cart', None)  # Remove 'cart' from session
    return JsonResponse({"message": "Cart cleared"})


@transaction.atomic
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_cart(request):
    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({"message": "Cart is empty"}, status=400)

    pharmacy_id = list(cart.keys())[0].split("_")[0]
    purchase = Purchase.objects.create(customer=request.user, pharmacy_id=pharmacy_id)

    for key, quantity in cart.items():
        _, drug_id = key.split("_")
        drug = get_object_or_404(Drug, id=drug_id)

        deduct_stock(drug, quantity)  # Deduct stock before creating PurchaseItem
        PurchaseItem.objects.create(purchase=purchase, drug=drug, quantity=quantity)

    request.session.pop('cart', None)
    return JsonResponse({"message": "Purchase completed", "purchase_id": purchase.id})


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        # Filter purchases by the logged-in user
        if self.request.user.is_staff:
            return super().get_queryset()  # Admins see all purchases
        return self.queryset.filter(customer=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the purchase with the logged-in user
        serializer.save(customer=self.request.user)


class PurchaseItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get_queryset(self):
        # Filter purchase items by purchases belonging to the logged-in user
        if self.request.user.is_staff:
            return super().get_queryset()  # Admins see all purchase items
        return self.queryset.filter(purchase__customer=self.request.user)
    @transaction.atomic
    def perform_create(self, serializer):
        purchase = serializer.validated_data.get('purchase')
        drug = serializer.validated_data.get('drug')
        quantity = serializer.validated_data.get('quantity')

        deduct_stock(drug, quantity)  # Deduct stock using the helper
        serializer.save()