from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import render 
from django.urls import reverse_lazy

from books import forms
from books.models import Product, Customer
from blog.models import PostPage


def index(request):
    posts = PostPage.objects.select_related().all().order_by('-date')

    return render(request, 'index.html', {
        'posts': posts,
    })


def order(request):
    products = Product.objects.all()
    return render(request, 'order.html', {
        'products': products,
        'key': settings.STRIPE_PUBLISHABLE,
    })


class MyLoginView(auth_views.LoginView):
    form_class = forms.MyAuthenticationForm


class GifteePasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/giftee_password_reset_confirm.html'
    success_url = reverse_lazy('dashboard')
    post_reset_login = True
