from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    text="Merhaba"
    context = {'text': text}
    return render(request, 'index.html', context)
