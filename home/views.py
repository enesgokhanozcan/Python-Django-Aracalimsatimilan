from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from home.models import Setting, ContactFormMessage, ContactForm
from product.models import Product, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata=Product.objects.all()[:3]
    category = Category.objects.all()
    context={'setting':setting,'page':'home','sliderdata':sliderdata,'category':category}
    return render(request, 'index.html', context)
def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting,'page':'aboutus'}
    return render(request, 'aboutus.html', context)
def references(request):
    setting = Setting.objects.get(pk=1)
    context={'setting':setting}
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
    form=ContactForm
    context={'setting':setting,'form':form}
    return render(request, 'contact.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {'products': products,'category':category}
    return HttpResponse(products,context)