from django.db import models
from decimal import Decimal
from django.shortcuts import render, redirect
from moneyed import Money
from ecommerce.apps.products.models import Product
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import m2m_changed



User = settings.AUTH_USER_MODEL

class Cart2(models.Model):
    card_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField("Date de création", auto_now_add=True)

    def __str__(self):
        return f"{self.card_id}"

    def __unicode__(self):
        return 


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='articles')
    cart = models.ForeignKey(Cart2, on_delete=models.CASCADE, verbose_name='panier')
    quantity = models.IntegerField("quantité")
    is_active = models.BooleanField("actif", default=True)
    
    
    def __str__(self):
        return f"{self.product}"

    # def __unicode__(self):
    #     return 


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            
        return cart_obj, new_obj
        
        
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='client', blank=True, null=True)
    products = models.ManyToManyField(Product, verbose_name='Articles', blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name='Prix Hors Taxe')
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2, verbose_name="Prix total TTC ")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    update = models.DateTimeField(auto_now=True, verbose_name='Mis à jour')
    
    objects = CartManager()
    
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'
        
    
    def __str__(self):
        return f"{self.id}" if self.id else self.email
    
    
    
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    print(f"Action effectuée : {action}")

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(f"Tous les articles du panier {instance.products.all()}")
        print(f"Prix total avant : {instance.total}")
        products = instance.products.all()
        total = 0
        quantity = 0
        for x in products:
            total += x.price 
            
            # I want to compute quantity and price together but, I got some trouble. Please check me this code.
            # total += Decimal(x.price) * Decimal(x.quantity)
        

        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
                

            
    

def pre_save_cart_receiver(sender, instance, *args, **kwargs):    
    zero = 0
    money_instance = Money(zero, 'GNF')
    insta = Money(instance.subtotal, 'GNF')
    if instance.subtotal > 0:
        # CALCUL DU PRIX TTC : TTC = HT + (1+ TVA%) EN GUINEE LA TVA EST DE 18% DONC 1+18% FERA 1.18
        instance.total = Decimal(instance.subtotal) * Decimal(1.18)
    else:
        instance.total = 0.00
    
    
    
pre_save.connect(pre_save_cart_receiver, sender=Cart)
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)
