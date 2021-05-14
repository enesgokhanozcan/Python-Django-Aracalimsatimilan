from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('TRUE','EVET'),
        ('FALSE','HAYIR'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True,max_length=300)
    keywords = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10,choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.title]  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])




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
    description = models.CharField(blank=True,max_length=300)
    keywords = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    price = models.FloatField()
    year = models.IntegerField()
    fuel = models.CharField(max_length=50)
    motor_power = models.IntegerField()
    engine_capacity = models.IntegerField()
    case_type = models.CharField(max_length=50)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

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



