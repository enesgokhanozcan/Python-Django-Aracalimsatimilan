from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, FileInput, Select
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from product.models import Category


class Menu(MPTTModel):
    STATUS = (
        ('TRUE','EVET'),
        ('FALSE','HAYIR'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True,max_length=300)
    keywords = models.CharField(blank=True,max_length=255)
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
        return reverse('content_detail', kwargs={'slug': self.slug})

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
TYPE = (
        ('menu', 'menu'),
        ('duyuru', 'duyuru'),
        ('ilan', 'ilan'),
    )
STATUS = (
        ('TRUE','TRUE'),
        ('FALSE','FALSE'),
    )

class Content(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    type = models.CharField(max_length=10, choices=TYPE)
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
        return reverse('content_detail', kwargs={'slug': self.slug})

    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="50"/>')
        else:
            return ""

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

class ContentForm(ModelForm):
    class Meta:
        model=Content
        fields=['type','title','description','keywords','image','price','year','fuel','motor_power','engine_capacity','case_type','detail','slug']
        widgets={
            'type': Select(attrs={'class': 'form-group', 'placeholder': 'Type'}, choices=TYPE),
            'title': TextInput(attrs={'class':'input','placeholder':'title'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'price'}),
            'year': TextInput(attrs={'class': 'input', 'placeholder': 'year'}),
            'fuel': TextInput(attrs={'class': 'input', 'placeholder': 'fuel'}),
            'motor_power': TextInput(attrs={'class': 'input', 'placeholder': 'motor_power'}),
            'engine_capacity': TextInput(attrs={'class': 'input', 'placeholder': 'engine_capacity'}),
            'case_type': TextInput(attrs={'class': 'input', 'placeholder': 'case_type'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'detail':CKEditorWidget(),

        }

class ContentImageForm(ModelForm):
    class Meta:
        model=CImages
        fields=['title','image']