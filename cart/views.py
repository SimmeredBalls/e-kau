from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from store.models import Product

# Create your views here.
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in cart_items)

    # Add subtotal per item (not stored in DB)
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'cart/view_cart.html', context)