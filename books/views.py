from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from books.models import Product, Membership
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
    memberships = Membership.objects.filter(customer__user=request.user)
    return render(request, 'dashboard/dashboard.html', {
        'memberships': memberships,
    })


@login_required
def product_page(request, product_slug):
    if product_slug == "hello-web-app":
        return redirect('hwa')
    elif product_slug == "hello-web-design":
        return redirect('hwd')

    return redirect('dashboard')


@login_required
def hwa(request):
    product_name = "Hello Web App"

    membership = Membership.objects.get(
        customer__user=request.user,
        product__name=product_name,
    )

    return render(request, 'dashboard/product/hello-web-app.html', {
        'membership': membership,
        'product_name': product_name,
    })


@login_required
def hwd(request):
    product_name = "Hello Web Design"

    membership = Membership.objects.get(
        customer__user=request.user,
        product__name=product_name,
    )

    return render(request, 'dashboard/product/hello-web-design.html', {
        'membership': membership,
        'product_name': product_name,
    })
