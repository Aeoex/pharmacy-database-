from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from permissions import IsAdminOrReadOnly
from .models import Pharmacy
from .serializers import PharmacySerializer

class PharmacyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing pharmacy instances.
    """
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes = [IsAdminOrReadOnly]  # Only admins users can modify

    def perform_create(self, serializer):

        serializer.save()
