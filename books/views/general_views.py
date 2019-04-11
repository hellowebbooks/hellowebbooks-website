from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from books import forms, helpers
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


def command_line_zine(request):
    """
    Form to create an account directly from the Command Line Zine landing page.
    """
    form_class = forms.ZineSignupForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # check if they already have an account
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Looks like we already have an account for this email address. Please log in and you can add the zine to your account from your dashboard.')
                return redirect('login')

            # create User account for email address
            user = helpers.create_user_from_email(email)

            # create Customer from user
            customer = Customer.objects.create(user=user)

            # set up Membership for the zine and tie to Customer
            product_obj = Product.objects.get(name="Really Friendly Command Line Intro")
            helpers.create_membership(customer, product_obj, paperback=False, video=True)

            # send over the reset password link to access account
            helpers.send_giftee_password_reset(
                request,
                user.email,
                "Admin Add",
                'registration/zine_signup_password_reset_subject.txt',
                'registration/zine_signup_password_reset_email.txt',
            )

            # add to convertkit
            if not settings.DEBUG:
                helpers.subscribe_to_newsletter(email, 'cmd-zine', has_paperback=False)

            # send email to admin
            mail_admins("Command line zine signup %s" % email, "Signed up on form on website")

            # success
            messages.success(request, 'Success! Check your email for the link to log in.')
            return redirect('learn-command-line')

    else:
        form = form_class()

    return render(request, 'learn-command-line.html', {
        'form': form,
    })
