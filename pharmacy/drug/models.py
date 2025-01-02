from django.db import models
from pharma.models import Pharmacy
from django.core.exceptions import ValidationError

class Drug(models.Model):
    DOSAGE_UNITS = [
        ('mcg', 'Microgram'),
        ('mg', 'Milligram'),
        ('g', 'Gram'),
        ('ml', 'Milliliter'),
        ('iu', 'International Unit'),
    ]
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.SET_NULL, related_name="drugs", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Drug Name")
    brand = models.CharField(max_length=50, verbose_name="Drug Brand")
    dosage_value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Drug Dosage Value"
    )
    dosage_unit = models.CharField(
        max_length=5, choices=DOSAGE_UNITS, verbose_name="Drug Dosage Unit"
    )
    quantity = models.PositiveIntegerField(verbose_name="Quantity in Stock")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per Unit"
    )
    production_date = models.DateField(verbose_name="Production Date")
    expiry_date = models.DateField(verbose_name="Expiry Date")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.brand}) - {self.dosage_value} {self.dosage_unit}"

    class Meta:
        verbose_name = "Drug"
        verbose_name_plural = "Drugs"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "dosage_value", "dosage_unit", "brand"],
                name="unique_drug_constraint"
            )
        ]

    def clean(self):
        if self.expiry_date <= self.production_date:
            raise ValidationError("Expiry date must be after the production date.")
