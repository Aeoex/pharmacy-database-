from rest_framework import serializers
from .models import PurchaseItem, Purchase
from django.db.models import Sum

class PurchaseItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()  # Add a custom field

    class Meta:
        model = PurchaseItem
        fields = ['id', 'drug', 'quantity', 'price', 'total_price']
        read_only_fields = ['id','price', 'total_price']  # Prevent frontend from modifying

    def get_total_price(self, obj):
        return obj.total_price  # Use the total_price property from the model
    
from django.db.models import Sum, F

class PurchaseSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ['id', 'customer', 'pharmacy', 'date', 'total_price']
        read_only_fields = ['id', 'date', 'total_price']

    def get_total_price(self, obj):
        # Calculate the total price of all PurchaseItems linked to this Purchase
        total = obj.items.aggregate(
            total_price=Sum(F('price') * F('quantity'))
        )['total_price']
        return total or 0  # Return 0 if no items exist

