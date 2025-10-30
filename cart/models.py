from django.db import models

# Create your models here.
from products.models import Product
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = True, null =True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.email if self.user else 'Anonymous'}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def subtotal(self):
        return self.product.price*self.quantity


    def __str__(self):
        return f"{self.product.name} and wuantity is {self.quantity}"