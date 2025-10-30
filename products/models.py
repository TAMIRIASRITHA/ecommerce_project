
from django.db import models
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('M','Men'),
        ('W','Women')
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    image = models.URLField(max_length=500, blank=True, null=True)  # Changed here
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='W')

    def __str__(self):
        return f"{self.name}"