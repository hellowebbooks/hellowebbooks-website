import json
import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins
from django.db import IntegrityError
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

from books import forms, options, helpers, coupon_codes
from books.models import Product, Membership, Customer
from blog.models import PostPage

stripe.api_key = os.environ['STRIPE_SECRET']

# FIXME: refactor the views into their own specialized view areas

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


@login_required
def dashboard(request):
    has_hwa = False
    has_hwd = False

    memberships = Membership.objects.filter(customer__user=request.user)
    for m in memberships:
        if m.product.name == "Hello Web App":
            has_hwa = True
        elif m.product.name == "Hello Web Design":
            has_hwd = True

    return render(request, 'dashboard/dashboard.html', {
        'memberships': memberships,
        'has_hwa': has_hwa,
        'has_hwd': has_hwd,
        # FIXME: Bad hack. Replace with temporary generated URLs on a private S3 file.
        'hwa_pdf': os.environ['HWA_PDF'],
        'hwa_epub': os.environ['HWA_EPUB'],
        'hwa_mobi': os.environ['HWA_MOBI'],
        'hwaic_pdf': os.environ['HWAIC_PDF'],
        'hwaic_epub': os.environ['HWAIC_EPUB'],
        'hwaic_mobi': os.environ['HWAIC_MOBI'],
        'hwd_pdf': os.environ['HWD_PDF'],
        'hwd_epub': os.environ['HWD_EPUB'],
        'hwd_mobi': os.environ['HWD_MOBI'],
    })


# FIXME: Are these needed anymore?
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


@login_required
def edit_email(request):
    user = request.user
    form_class = forms.EditEmailForm

    if request.method == 'POST':
        org_email = user.email
        form = form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email address has been updated!')
            return redirect('dashboard')

    else:
        form = form_class(instance=user)

    return render(request, 'dashboard/edit_email.html', {
        'form': form,
    })


def upsell(request, product):
    # User is logged in, go straight to buy page
    if request.user.is_authenticated and 'giftee_user' not in request.session:
        return redirect('/charge/%s' % product + '?coupon=customerfriend')
        #return redirect('charge', product=product)

    # Get someone to log in OR create an account
    form_class = forms.AddEmailForm

    if request.method == 'POST':
        request.session.pop('brand_new_user', None)
        form = form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.replace("@", "").replace(".", "")

            # check to see if they already have an account
            user = authenticate(username=username, password=password)

            if not user:
                # no user returned by authenticate either means wrong password
                # or no account
                try:
                    User.objects.get(email=email)
                except ObjectDoesNotExist:
                    # create new account
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                    )
                    request.session['brand_new_user'] = True
                    # XXX: Maybe don't log in the person? Because then
                    # if they return to the page, it gives them a discount
                    login(request, user)
                    return redirect('charge', product=product)

                # user wasn't found but the email exists in the system, so their
                # password must be wrong (or something)
                messages.error(request, 'Email address found in system but password did not match. Try again?')
                return redirect('upsell', product=product)

            else:
                # existing user was found and logged in
                login(request, user)
                return redirect('/charge/%s' % product + '?coupon=customerfriend')

    else:
        form = form_class()

    return render(request, 'order/upsell.html', {
        'form': form,
        'product': product,
    })


def gift(request, product):
    if request.method == 'POST':
        email = request.POST['gifteeEmail']
        message = request.POST['gifteeMessage']
        username = email.replace("@", "").replace(".", "")

        # FIXME: What should we do if someone *already* has an account?
        # Need to create a backend so I can log into the user without a
        # password re: https://stackoverflow.com/questions/6560182/django-authentication-without-a-password
        # PUNTING for now

        # Make sure there isn't a user account for this yet.
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            request.session['giftee_user'] = username
            request.session['giftee_email'] = email
            request.session['giftee_message'] = message
            return redirect('charge', product=product)

        mail_admins("Bad happenings on HWB", "Attempting to gift a product to someone who already has an account.")
        messages.error(request, "That person already has an account on Hello Web Books! This is a use-case that Tracy hasn't written the code for yet (whoops.) Please email tracy@hellowebbooks.com and she'll set it up manually with a discount for your trouble.")
        return redirect('upsell', product=product)


def charge(request, product=None):
    user = request.user

    # TODO: check whether we're going to this page with a coupon specified
    coupon_supplied = request.GET.get("coupon", None)

    amount, product_name, us_postage, can_postage, aus_postage, eur_postage, else_postage, paperback_price = helpers.product_details(product)
    product_obj, product_obj2, paperback, video, supplement = helpers.product_split(product)

    if request.method == "POST":
        gifted_product = False

        source = request.POST['stripeToken']
        amount = int(float(request.POST['paymentAmount'])) # rounds down in case of half numbers
        coupon = request.POST['stripeCoupon'] or ""

        has_paperback = False
        if request.POST['hasPaperback'] == 'true':
            has_paperback = True

        args = json.loads(request.POST['stripeArgs'])
        shipping = helpers.shipping_details(args)

        # Check whether this is a gifted product
        if 'giftee_user' in request.session:
            try:
                user = User.objects.create_user(
                    username=request.session['giftee_user'],
                    email=request.session['giftee_email'],
                    password=User.objects.make_random_password(),
                )
                gifted_product = True
            except IntegrityError as e:
                mail_admins("Bad happenings on HWB", "Attempting to gift a product to someone who already has an account.")
                messages.error(request, "That person already has an account on Hello Web Books! This is a use-case that Tracy hasn't written the code for yet (whoops.) Please email tracy@hellowebbooks.com and she'll set it up manually with a discount for your trouble.")
                return redirect('order')

        # See if they're already a customer if this is not a gift
        existing_customer = False
        gifted_customer = False
        if not gifted_product:
            try:
                customer = Customer.objects.get(user=request.user)
                id = customer.stripe_id
                existing_customer = True
                if customer.gift:
                    gifted_customer = True
            except Customer.DoesNotExist: # New customer
                pass

        # if the customer is buying something and their account was gifted,
        # the stripe customer needs to be wiped and replaced with a new customer
        if gifted_customer:
            # retrieve listing from stripe, delete
            cu = stripe.Customer.retrieve(customer.stripe_id)
            try:
                cu.delete()
            except stripe.error.InvalidRequestError:
                # customer not found on Stripe's end, might have already been deleted
                pass

        # create the stripe customer for the gifted-user or the new-user
        if gifted_product or not existing_customer or gifted_customer:
            id = helpers.create_stripe_customer(product, user, source, shipping, coupon)

        # charge the customer
        charge = stripe.Charge.create(
            customer=id,
            amount=amount, # set above POST
            currency='usd',
            description=product_name,
            shipping=shipping,
        )

        if not existing_customer:
            customer = Customer(
                stripe_id = id,
                last_4_digits = charge.source.last4,
                user = user,
                gift = gifted_product, # if this is a gifted product, then this'll be set to true
            )

        # gifted customer should have added their credit card by now, so we can
        # update their Customer object
        if gifted_customer:
            customer.stripe_id = id
            customer.last_4_digits = charge.source.last4,
            customer.gift = False

        # overwrite coupon if another is used
        if coupon:
            customer.coupon = coupon
        customer.save()

        # save the memberships in the database
        helpers.create_memberships(supplement, has_paperback, video, customer, product_obj, product_obj2)

        # send success email to admin
        helpers.send_admin_charge_success_email(user.email, product_name, has_paperback, supplement, gifted_product)

        # if this is a gifted product, send the person a gift email
        if 'giftee_user' in request.session:
            helpers.send_giftee_password_reset(request, user.email, product_name, request.session.get('giftee_message'))
            messages.success(request, "Success! We've sent an email to your giftee with how to access their files.")
            return redirect('order')

        # log in customer, redirect to their dashboard
        messages.success(request, "Success! You can access your product below.")
        request.session.pop('brand_new_user', None)
        return redirect('dashboard')

    else:
        form = forms.StripePaymentForm()

    # XXX: Also, we need to sign people up for our email newsleter correctly
    # after buying

    return render(request, "order/charge.html", {
        'form': form,
        'publishable_key': settings.STRIPE_PUBLISHABLE,
        'product': product,
        'paperback': paperback,
        'paperback_price': paperback_price,
        'amount': amount,
        'product_name': product_name,
        'us_postage': us_postage,
        'can_postage': can_postage,
        'eur_postage': eur_postage,
        'aus_postage': aus_postage,
        'else_postage': else_postage,
        'coupon_supplied': coupon_supplied,
    })


@login_required
def check_coupon(request):
    coupon = request.GET.get("coupon")
    format = request.GET.get("format")
    discount = 0

    if coupon in coupon_codes.COUPON_LOOKUP:
        discount = coupon_codes.COUPON_LOOKUP[coupon]

    if format == 'json':
        data = {
            'status': 'ok',
            'discount': discount,
        }

        return JsonResponse(data)

    data = {
        'status': 'fail',
    }
    return JsonResponse(data)


@login_required
def charge_update(request):
    user = request.user
    customer = get_object_or_404(Customer, user=user)
    last_4_digits = customer.last_4_digits

    if request.method == "POST":
        form = forms.StripePaymentForm(request.POST)

        if form.is_valid(): # charges the card
            cu = stripe.Customer.retrieve(customer.stripe_id)
            cu.card = form.cleaned_data['stripe_token']
            cu.save()

            customer.last_4_digits = form.cleaned_data['last_4_digits']
            customer.stripe_id = cu.id
            customer.save()

            messages.success(request, 'Your credit card has been updated!')
            return redirect('dashboard')
    else:
        form = forms.StripePaymentForm()

    return render(request, "order/charge_update.html", {
        'customer': customer,
        'last_4_digits': last_4_digits,
        'publishable_key': settings.STRIPE_PUBLISHABLE,
        'form': form,
    })


class MyLoginView(auth_views.LoginView):
    form_class = forms.MyAuthenticationForm


class GifteePasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/giftee_password_reset_confirm.html'
    success_url = reverse_lazy('dashboard')
    post_reset_login = True


@login_required
def course(request, product_slug, link=None):
    product_name = product_slug.replace("-", " ")
    product = Product.objects.get(name__iexact=product_name)
    course = options.course_list[product.name]

    membership = Membership.objects.get(
        customer__user=request.user,
        product__name=product.name,
    )

    # if default page, then show the intro page
    if not link:
        link = 'intro'

    # loop through options to get details for this course
    video_url, video_name, video_template, prev_link, prev_name, next_link, next_name = helpers.get_video_info_from_course(course, link)

    print(next_name)

    return render(request, "dashboard/course/course.html", {
        'product': product,
        'membership': membership,
        'course': course,
        'video_template': video_template,
        'video_name': video_name,
        'video_url': video_url,
        'prev_link': prev_link,
        'prev_name': prev_name,
        'next_link': next_link,
        'next_name': next_name,
        # FIXME: Bad hack. Replace with temporary generated URLs on a private S3 file.
        'hwa_pdf': os.environ['HWA_PDF'],
        'hwa_epub': os.environ['HWA_EPUB'],
        'hwa_mobi': os.environ['HWA_MOBI'],
        'hwaic_pdf': os.environ['HWAIC_PDF'],
        'hwaic_epub': os.environ['HWAIC_EPUB'],
        'hwaic_mobi': os.environ['HWAIC_MOBI'],
        'hwd_pdf': os.environ['HWD_PDF'],
        'hwd_epub': os.environ['HWD_EPUB'],
        'hwd_mobi': os.environ['HWD_MOBI'],
    })
