from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from blog.models import PostPage


def index(request):
    posts = PostPage.objects.select_related().all()
    return render(request, 'index.html', {
        'posts': posts,
    })

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {

    })
