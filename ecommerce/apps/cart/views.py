from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from ecommerce.apps.products.models import Product
from ecommerce.apps.cart.models import Cart2
from ecommerce.apps.cart.models import CartItem


def __cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    try:
        cart = Cart2.objects.get(card_id=__cart_id(request))
    except Cart2.DoesNotExist:
        cart = Cart2.objects.create(
            card_id=__cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
        
    return redirect('cart:main')
    




def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = get_object_or_404(Cart2, card_id=__cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
    except CartItem.DoesNotExist:
        pass
    template_name = 'cart/cart.html'
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, template_name, context)
