from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator



@login_required(login_url='/login/')
def receipe(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        return redirect('receipe')

    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(
            receipe_name__icontains=request.GET.get('search')
        )

    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'receipes': page_obj}
    return render(request, "receipe.html", context)


def update_receipe(request, id):
    queryset = get_object_or_404(Receipe, id=id)

    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get("receipe_image")
        receipe_name = data.get("receipe_name")
        receipe_description = data.get("receipe_description")

        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image

        queryset.save()
        return redirect('receipe')

    return render(request, 'update_receipe.html', {'receipe': queryset})


def delete_receipe(request, id):
    queryset = get_object_or_404(Receipe, id=id)
    queryset.delete()
    return redirect('receipe')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username not found')
            return redirect('login_page')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('login_page')

        login(request, user)
        return redirect('receipe')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('login_page')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register_page')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()

        messages.info(request, 'Account created Successfully')
        return redirect('register_page')

    return render(request, 'register.html')

def cart_page(request):
    return render(request, "cart.html")

def food_detail(request, id):
    # Database se specific recipe uthayenge ID ke basis par
    queryset = Receipe.objects.get(id = id)
    
    context = {
        'recipe': queryset,
        'page': queryset.receipe_name
    }
    return render(request, 'food_detail.html', context)