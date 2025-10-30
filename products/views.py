
from django.shortcuts import render, get_object_or_404

from products.models import Product
# Create your views here.


def product_list(request):
    query = request.GET.get('q')
    gender = request.GET.get('gender')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if gender:
        products = products.filter(category=gender)

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
        'selected_gender': gender,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'products/product_detail.html', {'product':product})