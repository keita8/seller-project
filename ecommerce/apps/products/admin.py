from dataclasses import fields
from django.contrib import admin
from .models import *
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin


class ProductResource(resources.ModelResource):
    title = Field(column_name="Article")
    price = Field(column_name="Prix")
    reference = Field(column_name="Reference")
    active = Field(column_name="En stock")

    class Meta:
        model = Product
        import_id_fields = ("reference",)
        fields = ("reference", "title", "price", "active")
        export_order = ("reference", "title", "price", "active")

    def dehydrate_title(self, obj):
        return obj.title

    def dehydrate_price(self, obj):
        return obj.price

    def dehydrate_reference(self, obj):
        return obj.reference

    def dehydrate_active(self, obj):
        if obj.active:
            return "Oui"
        return "Non"


# class BookAdmin(ExportActionMixin, admin.ModelAdmin):
#     pass

# @admin.register(Product)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ("reference", "title", "price", "quantity", "slug", "active")
    list_display_links = ("reference", "title", "price")
    readonly_fields = ("reference", "slug")
    search_fields = ("reference", "title", "price")
    list_editable = ("active",)
    list_filter = ("active",)



class CategorieAdmin(admin.ModelAdmin):
    list_display = ('categorie', 'is_public')
    list_editable = ('is_public', )
    search_field = ('categorie', )
    
    



class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')


admin.site.register(Product, ProductAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Variation, VariationAdmin)