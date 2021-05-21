from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Menu(MPTTModel):
    STATUS = (
        ('TRUE', 'EVET'),
        ('FALSE', 'HAYIR'),
    )
    parent=TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.CharField(blank=True,max_length=100)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by=['title']

    def __str__(self):
        full_path=[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return '/'.join(full_path[::-1])

class Content(models.Model):
    TYPE = (
        ('Menu', 'Menu'),
        ('Haber', 'Haber'),
        ('Duyuru', 'Duyuru'),
        ('Etkinlik', 'Etkinlik'),
    )
    STATUS = (
        ('TRUE','EVET'),
        ('FALSE','HAYIR'),
    )
    menu = models.OneToOneField(Menu,null=True,blank=True,on_delete= models.CASCADE) #relation with category table.
    type=models.CharField(max_length=10,choices=TYPE)
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True,max_length=300)
    keywords = models.CharField(blank=True,max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
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
    image_tag.short_descripton='Image'

    def get_absolute_url(self):
        return reverse('content_detail',kwargs={'slug':self.slug})

class CImages(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(blank=True,max_length=200)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""

    image_tag.short_descripton = 'Image'


