import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from content.models import Menu, Content, CImages
from home.forms import SearchForm
from home.models import Setting, ContactFormMessage, ContactForm
from product.models import Product, Category, Images


def index(request):
    current_user=request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    product_first = Product.objects.all().order_by('id')[:12]
    product_latest = Product.objects.all().order_by('-id')[:6]
    product_picked = Product.objects.all().order_by('-id')[:6]
    category = Category.objects.all()
    content_first = Content.objects.filter(type='ilan',status='TRUE').order_by('id')[:6]
    menu = Menu.objects.all()
    context={'setting' : setting,
             'page' : 'home',
             'sliderdata' : sliderdata,
             'category':category,
             'menu':menu,
             'product_latest':product_latest,
             'product_picked':product_picked,
             'product_first':product_first,
             'content_first':content_first}
    return render(request, 'index.html', context)
def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,'page':'aboutus','category': category}
    return render(request, 'aboutus.html', context)
def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,'category': category}
    return render(request, 'references.html', context)
def contact(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has been sent successfully... Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form=ContactForm
    context={'setting':setting,'form':form,'category': category}
    return render(request, 'contact.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'category': category,
               'products': products}
    return render(request, 'category_products.html', context)

def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category}
            return render(request, 'search_products.html', context)
    return HttpResponseRedirect('/')

def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      products_json = {}
      products_json = rs.title
      results.append(products_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context = {'category': category,
               'product': product,
               'images':images}
    return render(request, 'product_detail.html', context)

def menu(request,id):
    content = Content.objects.get(menu_id=id)
    if content:
        link='/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    else:
        messages.warning(request,"Opss! Something wrong...")
        link='/'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    try:
        content = Content.objects.get(pk=id)
        setting = Setting.objects.get(pk=1)
        images = CImages.objects.filter(content_id=id)
        context = {'content': content,
                   'category': category,
                   'menu': menu,
                   'images': images,
                   'setting': setting}
        return render(request, 'content_detail.html', context)

    except:
        messages.warning(request, " Error! Related content not found.")
        link = '/error'
        return HttpResponseRedirect(link)
