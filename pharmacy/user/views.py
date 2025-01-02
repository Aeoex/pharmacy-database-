from django.http import JsonResponse
from .models import CustomUser, AdminProfile
from .serializers import CustomUserSerializer, AdminProfileSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
import random , string
from pharma.models import Pharmacy



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):

        if self.request.user.is_staff:
            return CustomUser.objects.all()  # admins see all users
        return CustomUser.objects.filter(pharmacy=self.request.user.pharmacy)  # normal users see users from their pharmacy

    @action(detail=True, methods=['get'])
    def admin_profile(self, request, pk=None):
        """
        Custom action to retrieve Admin Profile for a user
        """
        user = self.get_object()
        try:
            admin_profile = user.admin_profile
            serializer = AdminProfileSerializer(admin_profile)
            return Response(serializer.data)
        except AdminProfile.DoesNotExist:
            return JsonResponse({"error": "Admin profile does not exist for this user."}, status=404)
        


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminUser]  

    def get_queryset(self):
        if self.request.user.is_staff:
            return AdminProfile.objects.all()  # Admins see all admin profiles
        return AdminProfile.objects.filter(user=self.request.user)  # Users see their own admin profile

    def perform_create(self, serializer):
        # Custom logic for creating admin profiles can go here (like associating with the user)
        user = self.request.user
        serializer.save(user=user)



@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def register_user(request):
    """
    Endpoint to register a new user.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    pharmacy_id = 1 #request.data.get("pharmacy")

    if not username or not password or not pharmacy_id:
        return Response({"error": "Username, password, and pharmacy are required."}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # Assign random values for email, contact number, and address
    email = f"{username}@example.com"
    contact_number = f"{random.randint(1000000000, 9999999999)}"  # Random 10-digit number
    address = ''.join(random.choices(string.ascii_letters + string.digits, k=15))  # Random alphanumeric string

    try:
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    except Pharmacy.DoesNotExist:
        return Response({"error": "Invalid pharmacy ID."}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        contact_number=contact_number,
        user_address=address,
        pharmacy=pharmacy
    )
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "User created successfully.",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)
    


