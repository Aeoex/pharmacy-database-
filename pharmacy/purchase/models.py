from django.db import models
from drug.models import Drug
from pharma.models import Pharmacy
from user.models import CustomUser

class Purchase(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="purchases")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.id} by {self.customer} at {self.pharmacy}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name="purchase_items")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity of Item")
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Price per unit",default=0)

    def __str__(self):
        return f"{self.quantity} of {self.drug} for {self.purchase}"

    @property
    def total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if self.drug:
            self.price = self.drug.price
        super().save(*args, **kwargs)