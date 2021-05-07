from django.contrib import admin

# Register your models here.
from product.models import Category, Product, Images
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status','image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','image','image_tag','status']
    list_filter = ['status']
    inlines = [ProductImageInline]
    readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'image','image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)