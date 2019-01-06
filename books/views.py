from django.shortcuts import render
from django.core.mail import mail_admins

from blog.models import PostPage

# Create your views here.
def index(request):
    posts = PostPage.objects.select_related().all()
    mail_admins(
        "Hey the email integration works",
        "This",
    )

    return render(request, 'index.html', {
        'posts': posts,
    })
