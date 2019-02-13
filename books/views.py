from django.shortcuts import render
from django.core.mail import mail_admins

from blog.models import PostPage

# Create your views here.
def index(request):
    posts = PostPage.objects.select_related().all().order_by('-date')

    for post in posts:
        print(post.date)

    return render(request, 'index.html', {
        'posts': posts,
    })
