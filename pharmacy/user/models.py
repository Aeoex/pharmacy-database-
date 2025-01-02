from django.contrib.auth.models import AbstractUser
from django.db import models
from pharma.models import Pharmacy

class CustomUser(AbstractUser):
    pharmacy = models.ForeignKey(Pharmacy,on_delete=models.CASCADE,related_name="users",null=True)
    contact_number = models.CharField(max_length=15, verbose_name="Contact Number", null=True, blank=True)
    user_address = models.CharField(max_length=400, verbose_name="User Address", null=True, blank=True)

    def __str__(self):
        return self.username

class AdminProfile(models.Model):
    ADMIN_SHIFT_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night','Night'),
    )
    working_at = models.ForeignKey(Pharmacy,on_delete=models.CASCADE,related_name="admins",null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    shift = models.CharField(max_length=10, choices=ADMIN_SHIFT_CHOICES, default='morning')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary")

    def __str__(self):
        return f"{self.user.username} - Admin"
