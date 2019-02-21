import json
import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy

from books import forms, options, coupon_codes
from books.models import Product, Membership, Customer
from blog.models import PostPage

stripe.api_key = os.environ['STRIPE_SECRET']


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
        username = email.replace("@", "").replace(".", "")
        password = User.objects.make_random_password()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        request.session['giftee_user'] = True
        login(request, user)
        return redirect('charge', product=product)

    messages.error(request, "How'd you get here?")
    return redirect('order')


@login_required
def charge(request, product=None):
    user = request.user
    hwb_bundle = False
    amount = 0
    product_name = ""
    us_postage = 0
    can_postage = 0
    aus_postage = 0
    else_postage = 0
    paperback_price = 0

    # check whether we're going to this page with a coupon specified
    coupon_supplied = request.GET.get("coupon", None)

    try:
        amount = options.PRODUCT_LOOKUP[product].amount
        product_name = options.PRODUCT_LOOKUP[product].description
        us_postage = options.PRODUCT_LOOKUP[product].us_postage
        can_postage = options.PRODUCT_LOOKUP[product].can_postage
        aus_postage = options.PRODUCT_LOOKUP[product].aus_postage
        eur_postage = options.PRODUCT_LOOKUP[product].eur_postage
        else_postage = options.PRODUCT_LOOKUP[product].else_postage
        paperback_price = options.PRODUCT_LOOKUP[product].paperback_addl
    except KeyError:
        messages.error(request, "Product not found.")
        mail_admins("Bad happenings on HWB", "Product not found in order page: [%s]" % (product))
        print(amount)
        print(product_name)
        print(us_postage)
        print(can_postage)
        print(aus_postage)
        print(eur_postage)
        print(else_postage)
        print(paperback_price)
        return redirect('order')

    # TODO: This is probably a bad way of doing this. Look into something
    # more future-proof.
    split_product = product.split("-")
    if split_product[0] == "hwa":
        product_obj = Product.objects.get(name="Hello Web App")
    elif split_product[0] == "hwd":
        product_obj = Product.objects.get(name="Hello Web Design")
    elif split_product[0] == "hwb":
        hwb_bundle = True
        product_obj = Product.objects.get(name="Hello Web App")
        product_obj2 = Product.objects.get(name="Hello Web Design")

    paperback = False
    if split_product[1] == "pb":
        paperback = True
        print(paperback)

    video = False
    if split_product[1] == "video":
        video = True

    supplement = False
    if len(split_product) == 3:  # three arguments means it's an update to pkg
        supplement = True

    if request.method == "POST":
        source = request.POST['stripeToken']
        amount = int(float(request.POST['paymentAmount'])) # rounds down in case of half numbers
        coupon = request.POST['stripeCoupon'] or ""
        has_paperback = False
        if request.POST['hasPaperback'] == 'true':
            has_paperback = True
        args = json.loads(request.POST['stripeArgs'])

        # XXX: Omg Tracy write some tests

        # XXX: Still need to figure out the system for fulfilling print orders
        shipping = {
            'name': '',
            'address': {
                'line1': '',
                'line2': '',
                'city': '',
                'country': '',
                'postal_code': '',
                'state': '',
            }
        }
        for key, value in args.items():
            if key == "shipping_address_line1":
                shipping['address']['line1'] = value
            elif key == 'shipping_address_line2':
                shipping['address']['line2'] = value
            elif key == 'shipping_address_city':
                shipping['address']['city'] = value
            elif key == 'shipping_address_country_code':
                shipping['address']['country'] = value
            elif key == 'shipping_address_zip':
                shipping['address']['postal_code'] = value
            elif key == 'shipping_address_state':
                shipping['address']['state'] = value
            elif key == 'shipping_name':
                shipping['name'] = value

        #print(shipping)

        # See if they're already a customer
        try:
            customer = Customer.objects.get(user=request.user)
            existing_customer = True
            id = customer.stripe_id
        except Customer.DoesNotExist: # New customer
            existing_customer = False
            customer = None

            stripe_customer = dict(
                description=user,
                email=user.email,
                card=source,
                shipping=shipping,
            )

            if coupon:
                stripe_customer['coupon'] = coupon

            try:
                customer = stripe.Customer.create(**stripe_customer)
                id = customer.id
            except stripe.error.CardError as e:
                body = e.json_body
                err  = body.get('error', {})
                messages.error(request, err.message)
                return redirect('charge', product=product)
            except stripe.error.StripeError as e:
                if e.param == 'coupon':
                    messages.error(request, 'Sorry, that coupon is invalid!')
                else:
                    messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
                    mail_admins("Bad happenings on HWB", "Payment failure for [%s] - [%s]" % (user.email, e))
                return redirect('charge', product=product)

        # charge the customer!
        print(id)
        charge = stripe.Charge.create(
            customer=id,
            amount=amount, # set above POST
            currency='usd',
            description=product_name,
            shipping=shipping,
        )

        if not existing_customer: # create the customer object
            cus = Customer(
                stripe_id = id,
                last_4_digits = charge.source.last4,
                user = user,
            )

            # XXX: This might not be saved in the database, check this
            if coupon:
                cus.coupon = coupon

            cus.save()
            customer = cus

        # XXX: If video supplement, need to grab existing membership and add
        if supplement:
            try:
                membership = Membership.objects.get(customer=customer, product=product_obj)
                membership.video = True
                membership.save()
            except Membership.DoesNotExist:
                # How'd this happen?
                messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
                mail_admins("Bad happenings on HWB", "Payment failure for [%s] - Buying supplement but membership doesn't exist" % (user.email))

        else: # not supplement, make a whole new membership
            print("making membership")
            print("paperback?")
            print(paperback)
            membership = Membership(
                customer = customer,
                product = product_obj,
                paperback = has_paperback, # set from form after if statement
                video = video, # set before POST if statement
            )
            membership.save()

            if hwb_bundle:
                membership2 = Membership(
                    customer = customer,
                    product = product_obj2,
                    paperback = has_paperback, # set from form after if statement
                    video = video, # set before POST if statement
                )
                membership2.save()

        # send email to admin
        # XXX: Need to pass along shipping details too
        send_mail(
            'New paying customer',
            '%s bought %s. Supplement: %s. Woohoo!' % (user.email, product_name, supplement),
            'noreply@hellowebbooks.com',
            ['tracy@hellowebbooks.com'],
        )

        # XXX: Wait, the giftee should probably be notified
        # who gifted the package
        if 'giftee_user' in request.session:
            form = PasswordResetForm({'email': user.email})
            assert form.is_valid()
            # XXX: Need to test this AND create a custom template
            # XXX: Don't forget the email subject line
            # XXX: Package name is incorrect
            # XXX: Also we need to go to the correct page after confirmation. Or log in?
            form.save(
                request=request,
                from_email="tracy@hellowebbooks.com",
                email_template_name='registration/giftee_password_reset_email.txt',
                extra_email_context={ 'product': product.name },

            )
            logout(request)
            messages.success(request, "Success! We've sent an email to your giftee with how to access their files.")
            return redirect('order')

        # log in customer, redirect to their dashboard
        messages.success(request, "Success! You can access your product below.")
        request.session.pop('brand_new_user', None)
        return redirect('dashboard')

    else:
        form = forms.StripePaymentForm()

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

        #'stripe_profile': stripe_profile,
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
