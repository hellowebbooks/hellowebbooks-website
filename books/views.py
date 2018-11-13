from django.shortcuts import render

from blog.models import PostPage

# Create your views here.
def index(request):
    posts = PostPage.objects.select_related().all()
    return render(request, 'index.html', {
        'posts': posts,
    })
