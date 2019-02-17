import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from books import forms, options, coupon_codes
from books.models import Product, Membership, Customer
from blog.models import PostPage

stripe.api_key = os.environ['STRIPE_SECRET']


def index(request):
    posts = PostPage.objects.select_related().all().order_by('-date')

    for post in posts:
        print(post.date)

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
    # XXX: Need a flow for if someone is buying as a gift :O

    # User is logged in, go straight to buy page
    if request.user.is_authenticated:
        return redirect('charge', product=product)

    # XXX: Uh also we need to upsell the paperbacks for the video package buyers

    # Get someone to log in OR create an account
    form_class = forms.AddEmailForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.replace("@", "").replace(".", "")

            # XXX Test for username uniqueness
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            return redirect('charge', product=product)

    else:
        form = form_class()

    return render(request, 'order/upsell.html', {
        'form': form,
    })


@login_required
def charge(request, product=None):
    user = request.user
    hwb_bundle = False
    paperback = False
    amount = 0
    product_name = ""

    try:
        amount = options.PRODUCT_LOOKUP[product].amount
        product_name = options.PRODUCT_LOOKUP[product].description
    except KeyError:
        messages.error(request, "Product not found.")
        mail_admins("Bad happenings on HWB", "Product not found in order page: [%s]" % (product))
        return redirect('order')

    # TODO: This is probably a bad way of doing this. Look into something
    # more future-proof.
    split_product = product.split("-")
    if split_product[0] == "hwa":
        product = Product.objects.get(name="Hello Web App")
    elif split_product[0] == "hwd":
        product = Product.objects.get(name="Hello Web Design")
    elif split_product[0] == "hwb":
        hwb_bundle = True
        product = Product.objects.get(name="Hello Web App")
        product2 = Product.objects.get(name="Hello Web Design")

    if split_product[1] == "pb":
        paperback = True

    if request.method == "POST":
        print("in post")
        source = request.POST['stripeToken']
        print(source)
        print("payment?")
        print(request.POST['paymentAmount'])
        print("coupon?")
        coupon = request.POST['stripeCoupon']
        print(coupon)
        print("args?")
        print(request.POST['stripeArgs'])

        #form = forms.StripePaymentForm(request.POST)
        #is_stripe_valid = True
        coupon = ""


        stripe_customer = dict(
            description=user,
            email=user.email,
            card=source,
        )

        if coupon:
            stripe_customer['coupon'] = coupon

        try:
            customer = stripe.Customer.create(**stripe_customer)
            is_stripe_valid = True
        except stripe.error.CardError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, err.message)
        except stripe.error.StripeError as e:
            if e.param == 'coupon':
                messages.error(request, 'Sorry, that coupon is invalid!')
            else:
                messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
                mail_admins("Bad happenings on HWB", "Payment failure for [%s]" % (user.email))

        # charge the customer!
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount, # set above POST
            currency='usd',
            description='My one-time charge',
        )

        cus = Customer(
            stripe_id = customer.id,
            last_4_digits = charge.source.last4,
            user = user,
        )

        if coupon:
            cus.coupon = coupon

        cus.save()

        # XXX Deal with the paperback / video cases
        membership = Membership(
            customer = cus,
            product = product,
            paperback = True,
            video = False,
        )
        membership.save()

        if hwb_bundle:
            membership2 = Membership(
                customer = cus,
                product = product2,
                paperback = True,
                video = False,
            )
            membership2.save()

        # send email to admin
        send_mail(
            'New paying customer',
            '%s bought a book. Woohoo!' % (user.email),
            'noreply@hellowebbooks.com',
            ['tracy@hellowebbooks.com'],
        )

        # log in customer, redirect to their dashboard
        return redirect('dashboard')




        """
        if form.is_valid(): # charges the card
            # create the Stripe customer from the token submitted
            is_stripe_valid = False
            customer = None
            sub = ""

            stripe_customer = dict(
                description=user,
                email=user.email,
                card=form.cleaned_data['stripe_token'],
            )

            if form.cleaned_data['coupon']:
                coupon = form.cleaned_data['coupon']
                stripe_customer['coupon'] = coupon

            try:
                customer = stripe.Customer.create(**stripe_customer)
                is_stripe_valid = True
            except stripe.error.CardError as e:
                body = e.json_body
                err  = body.get('error', {})
                messages.error(request, err.message)
            except stripe.error.StripeError as e:
                if e.param == 'coupon':
                    messages.error(request, 'Sorry, that coupon is invalid!')
                else:
                    messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
                    mail_admins("Bad happenings on HWB", "Payment failure for [%s]" % (user.email))

            # charge the customer!
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=amount, # set above POST
                currency='usd',
                description='My one-time charge',
            )

        # still valid? lol
        if form.is_valid() and is_stripe_valid:
            print("still valid")
            cus = Customer(
                stripe_id = customer.id,
                last_4_digits = form.cleaned_data['last_4_digits'],
                user = user,
            )

            if coupon:
                cus.coupon = coupon

            cus.save()

            # XXX Deal with the paperback / video cases
            membership = Membership(
                customer = cus,
                product = product,
                paperback = True,
                video = False,
            )
            membership.save()

            if hwb_bundle:
                membership2 = Membership(
                    customer = cus,
                    product = product2,
                    paperback = True,
                    video = False,
                )
                membership2.save()

            # send email to admin
            send_mail(
                'New paying customer',
                '%s bought a book. Woohoo!' % (user.email),
                'noreply@hellowebbooks.com',
                ['tracy@hellowebbooks.com'],
            )

            # log in customer, redirect to their dashboard
            return redirect('dashboard')

        else:
            return render(request, "order/charge.html", {
                'form': form,
                'publishable_key': settings.STRIPE_PUBLISHABLE,
                'product': product
            })
            """
    else:
        form = forms.StripePaymentForm()

    return render(request, "order/charge.html", {
        'form': form,
        'publishable_key': settings.STRIPE_PUBLISHABLE,
        'product': product,
        'paperback': paperback,
        'amount': amount,
        'product_name': product_name,
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

    return render(request, "dashboard/charge_update.html", {
        'customer': customer,
        'last_4_digits': account.last_4_digits,
        'publishable_key': settings.STRIPE_PUBLISHABLE,
        'form': form,
    })


@login_required
def charge_cancel(request, directory=None):
    """
    If a vendor clicks the button to cancel their paid account, this changes
    them back to a free account.
    """
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    account = get_object_or_404(StripeProfile, profile=profile)
    plan_name = profile.payment_method
    company_name = profile.company_name

    cu = stripe.Customer.retrieve(account.stripe_id)
    #import pdb; pdb.set_trace()
    subs = stripe.Subscription.all(customer=cu)
    for sub in subs:
        sub.delete()

    profile.is_pro_profile = False
    profile.online = False
    profile.payment_method = ""
    profile.save()

    account.delete()

    # send email to admin
    send_mail(
        'WeddingLovely vendor subscription cancel',
        '%s just cancelled their %s account. Boo!' % (company_name, plan_name),
        'noreply@weddinglovely.com',
        ['admin@weddinglovely.com']
    )

    # send email to customer
    template_cus = get_template('shared/sales/cancel_customer_email.txt')
    context_cus = Context({
        'company_name': company_name,
        'directory' : "WeddingLovely",
    })
    content_cus = template_cus.render(context_cus)

    send_mail(
        'Your account has been downgraded on WeddingLovely',
        content_cus,
        'yesreply@weddinglovely.com',
        [user.email],
    )

    messages.info(request, 'Your upgraded account has been cancelled and your profile downgraded. Let us know what we can do to improve!')
    return redirect('profile_dashboard')
