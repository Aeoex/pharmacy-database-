from django.contrib import admin
from .models import CustomUser, AdminProfile

class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [AdminProfileInline]

admin.site.register(CustomUser, CustomUserAdmin)