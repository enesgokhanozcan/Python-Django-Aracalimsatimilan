from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from django.utils.safestring import mark_safe


class Category(models.Model):
    STATUS = (
        ('TRUE','EVET'),
        ('FALSE','HAYIR'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField()
    parent =models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""


class Product(models.Model):
    STATUS = (
        ('TRUE','EVET'),
        ('FALSE','HAYIR'),
    )
    category = models.ForeignKey(Category,on_delete= models.CASCADE) #relation with category table.
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    price = models.FloatField()
    year = models.IntegerField()
    fuel = models.CharField(max_length=50)
    motor_power = models.IntegerField()
    engine_capacity = models.IntegerField()
    case_type = models.CharField(max_length=50)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""

class Images(models.Model):
        product=models.ForeignKey(Product,on_delete=models.CASCADE)
        title = models.CharField(max_length=200,blank=True)
        image = models.ImageField(blank=True, upload_to='images/')

        def __str__(self):
            return self.title

        def image_tag(self):
            if self.image:
                return mark_safe(f'<img src="{self.image.url}" height="50"/>')
            else:
                return ""



