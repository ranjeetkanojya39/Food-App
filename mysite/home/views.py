from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.



def home(request):
    return render(request, "home/index.html" )


def succsess_page(request):
    return HttpResponse("<h1>Succsess Page</h1>")

def about(request):
    context = {'page': 'about_page'}
    return render(request, "home/about.html",context)

def contact(request):
    context = {'page' : 'contact_page'}
    return render(request, "home/contact.html",context)


