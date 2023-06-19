from django.contrib import admin
from .models import Product,ReviewRating,Wishlist,Carousel
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

class CarouselAdmin(admin.ModelAdmin):
    list_display=('images',)
    list_display_links=('images',)
    
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating)
admin.site.register(Carousel,CarouselAdmin)
admin.site.register(Wishlist)