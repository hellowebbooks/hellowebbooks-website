from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from books.models import Product
from blog.models import PostPage


def index(request):
    posts = PostPage.objects.select_related().all()
    return render(request, 'index.html', {
        'posts': posts,
    })


def order(request):
    # XXX: Probably want to remove the below and
    # keep the order stuff to manual listings for now.
    products = Product.objects.all()
    return render(request, 'order.html', {
        'products': products,
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {

    })
