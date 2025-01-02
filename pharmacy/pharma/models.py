from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=50,verbose_name="Pharmacy Name")
    address = models.CharField(max_length=400,verbose_name="Pharmacy Address",unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pharmacy"
        verbose_name_plural = "Pharmacies"
        ordering = ["name"]  # Sort by name alphabetically