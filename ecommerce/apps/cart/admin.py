from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'subtotal', 'total', 'update', 'timestamp')
    list_display_links = ('user',)
    search_fields = ('user', )
    
    
    
@admin.register(Cart2)
class CartAdmin(admin.ModelAdmin):
    list_display = ('card_id', 'date_added')




@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')
    search_fields = ('product', 'cart', 'quantity',)