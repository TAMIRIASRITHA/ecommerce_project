
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.


def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    total = sum(item.subtotal for item in cart.items.all())
    return render(request, 'cart/cart.html',{'cart':cart, 'total':total})
    



@login_required
def add_to_cart(request, product_id):
    print(product_id)

    print(request)
    product = get_object_or_404(Product, id=product_id)
    print("product")
    print(product)
    cart = Cart.objects.get_or_create(user=request.user)
    print(cart)
    item, created = CartItem.objects.get_or_create(cart=cart[0], product=product)
    if not created:
        item.quantity +=1
        item.save()
    else:
        item.quantity = 1
    return redirect('cart:view_cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id = item_id)
    item.delete()
    return redirect('cart:view_cart')
    
#quantity update view
@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.GET.get('action')

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart:view_cart')    