from django.contrib import admin
from .models import Purchase, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1  # Number of empty forms to display by default
    readonly_fields = ("total_price",)  # Makes the total_price field read-only
    fields = ("drug", "quantity", "total_price")

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "pharmacy", "date")
    list_filter = ("pharmacy", "date")  # Adds filters for pharmacy and date
    search_fields = ("customer__username", "pharmacy__name")  # Allows search by customer and pharmacy
    inlines = [PurchaseItemInline]  # Includes PurchaseItem inline in Purchase admin
    readonly_fields = ()  
    date_hierarchy = "date"  # Adds date hierarchy navigation

@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("id", "purchase", "drug", "quantity")
    search_fields = ("purchase__id", "drug__name")  # Allows search by purchase ID and drug name
    list_filter = ("drug",)  # Adds a filter for drugs
    readonly_fields = ("price","total_price",)  # Makes the total_price field read-only

    def price(self, obj):
        return obj.drug.price
    price.short_description = "Price per unit"