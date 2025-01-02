from rest_framework import serializers
from .models import Drug

class DrugSerializer(serializers.ModelSerializer):
    pharmacy = serializers.StringRelatedField()

    class Meta:
        model = Drug
        fields = [
            'id', 'pharmacy', 'name', 'brand', 'dosage_value', 
            'dosage_unit', 'quantity', 'price', 
            'production_date', 'expiry_date', 'updated'
        ]
        read_only_fields = ['id', 'updated']