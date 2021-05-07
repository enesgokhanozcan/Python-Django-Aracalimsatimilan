from django.contrib import admin

# Register your models here.
from product.models import Category, Product, Images
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['status']
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','status']
    list_filter = ['status']
    inlines = [ProductImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)