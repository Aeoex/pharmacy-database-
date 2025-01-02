from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from permissions import IsAdminOrReadOnly
from .models import Drug
from .serializers import DrugSerializer

class DrugViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting drug instances with filtering and searching.
    """
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # Add filtering and searching backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Specify fields for filtering
    filterset_fields = ['pharmacy', 'dosage_unit', 'brand', 'expiry_date']

    # Specify fields for search
    search_fields = ['name', 'brand', 'pharmacy__name']

    # Specify fields for ordering
    ordering_fields = ['price', 'expiry_date', 'name']
    ordering = ['name']  # Default ordering by name

    def perform_create(self, serializer):
        serializer.save()
