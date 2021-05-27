from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, ContentForm
from home.models import Setting
from product.models import Category
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile

def index(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
        'profile': profile,
        'setting': setting,
        'menu': menu
    }
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !!!  Username or Password is incorrect")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context = {'category': category}
    return render(request,'login.html',context)


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'category': category
                       })


@login_required(login_url='/login')
def contents(request):
    category=Category.objects.all()
    setting = Setting.objects.get(pk=1)
    menu=Menu.objects.all()
    current_user=request.user
    contents=Content.objects.filter(user_id=current_user.id)
    context={
        'category':category,
        'menu':menu,
        'setting': setting,
        'contents':contents,
    }
    return  render(request,'user_content.html',context)

@login_required(login_url='/login')
def addcontent(request):
    if request.method=='POST':
        form=ContentForm(request.POST,request.FILES)
        if form.is_valid():
            current_user=request.user
            data=Content()
            data.user_id=current_user.id
            data.title=form.cleaned_data['title']
            data.description = form.cleaned_data['description']
            data.keywords = form.cleaned_data['keywords']
            data.image = form.cleaned_data['image']
            data.price = form.cleaned_data['price']
            data.year = form.cleaned_data['year']
            data.fuel = form.cleaned_data['fuel']
            data.motor_power = form.cleaned_data['motor_power']
            data.engine_capacity = form.cleaned_data['engine_capacity']
            data.case_type = form.cleaned_data['case_type']
            data.slug = form.cleaned_data['slug']
            data.status='False'
            data.save()
            messages.success(request,'Your content ınserted susccessfully')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error:'+ str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        form=ContentForm()
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        context = {
            'category': category,
            'menu': menu,
            'setting': setting,
            'form': form}
        return render(request,'user_addcontent.html',context)

@login_required(login_url='/login')
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Content Updated Successfuly.')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error:' +str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' +str(id))
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'menu': menu,
            'setting': setting,
            'form': form}
        return render(request, 'user_addcontent.html', context)


@login_required(login_url='/login')
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted.')
    return HttpResponseRedirect('/user/contents')