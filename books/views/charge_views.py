import json
import os
import stripe

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from books import forms, helpers, coupon_codes
from books.models import Customer

stripe.api_key = os.environ['STRIPE_SECRET']


# TODO: Set up something so people who made accounts but haven't bought
# anything are tracked.
# TODO: This view should be renamed to log in or create account
def upsell(request, product_slug=None):
    # User is logged in, go straight to buy page (as long as they're not a
    # gifted user or someone who made a log in but hasn't bought yet.)
    if request.user.is_authenticated and 'giftee_user' not in request.session and 'brand_new_user' not in request.session:
        return redirect('/charge/%s' % product_slug + '?coupon=customerfriend')

    # if they went through upsell page but haven't bought anything, go to charge
    # page without the coupon
    if request.user.is_authenticated and 'brand_new_user' in request.session:
        return redirect('/charge/%s' % product_slug)

    # grab coupon if supplied
    coupon_supplied = request.GET.get("coupon", None)

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
                    # FIXME: Maybe don't log in the person? Because then
                    # if they return to the page, it gives them a discount
                    login(request, user)
                    if coupon_supplied:
                        return redirect('/charge/' + product_slug + '/?coupon=' + coupon_supplied)
                    return redirect('charge', product_slug=product_slug)

                # user wasn't found but the email exists in the system, so their
                # password must be wrong (or something)
                messages.error(request, 'Email address found in system but password did not match. Try again?')
                if coupon_supplied:
                    return redirect('/buy/' + product_slug + '/?coupon=' + coupon_supplied)
                return redirect('upsell', product_slug=product_slug)

            else:
                # existing user was found and logged in
                login(request, user)
                if coupon_supplied:
                    return redirect('/charge/%s' % product_slug + '/?coupon=' + coupon_supplied)
                return redirect('/charge/%s' % product_slug + '/?coupon=customerfriend')

    else:
        form = form_class()

    return render(request, 'order/upsell.html', {
        'form': form,
        'product': product_slug,
        'coupon_supplied': coupon_supplied,
    })


def gift(request, product_slug):
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
            return redirect('charge', product_slug=product_slug)

        mail_admins("Bad happenings on HWB", "Attempting to gift a product to someone who already has an account.")
        messages.error(request, "That person already has an account on Hello Web Books! This is a use-case that Tracy hasn't written the code for yet (whoops.) Please email tracy@hellowebbooks.com and she'll set it up manually with a discount for your trouble.")
        return redirect('upsell', product_slug=product_slug)

    messages.error(request, 'How did you get here? Email tracy@hellowebbooks.com if you need help!')
    return redirect('order')


def charge(request, product_slug=None):
    user = request.user
    if not user.is_authenticated and 'giftee_user' not in request.session:
        messages.error(request, "Please choose a product and sign in or create an account first.")
        return redirect('order')

    # grab coupon if supplied
    coupon_supplied = request.GET.get("coupon", None)

    amount, product_name, us_postage, can_postage, aus_postage, eur_postage, else_postage, paperback_price = helpers.product_details(product_slug)
    product_obj, product_obj2, paperback, video, supplement = helpers.product_split(product_slug)

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
        if gifted_product or not existing_customer or gifted_customer or not id:
            # XXX: confirm that the customer object of gifter is overridden by
            # the new customer object in Stripe
            id = helpers.create_stripe_customer(request, product_slug, user, source, shipping, coupon)

        # charge the customer
        try:
            charge = stripe.Charge.create(
                customer=id,
                amount=amount, # set above POST
                currency='usd',
                description=product_name,
                shipping=shipping,
            )
        except stripe.error.CardError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, err.get('message'))
            return redirect('charge', product_slug=product_slug)
        except stripe.error.InvalidRequestError as e:
            messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
            mail_admins("Stripe Invalid Request Errror on HWB", "Payment failure for [%s] - [%s]" % (user.email, e))
            return redirect('charge', product_slug=product_slug)
        except stripe.error.StripeError as e:
            messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
            mail_admins("Bad happenings on HWB", "Payment failure for [%s] - [%s]" % (user.email, e))
            return redirect('charge', product_slug=product_slug)

        if not existing_customer:
            customer = Customer(
                stripe_id = id,
                last_4_digits = charge.source.last4,
                user = user,
                gift = gifted_product, # if this is a gifted product, then this'll be set to true
            )

        # gifted customer should have added their credit card by now, so we can
        # update their Customer object
        if gifted_customer or not customer.stripe_id:
            customer.stripe_id = id
            customer.last_4_digits = charge.source.last4,
            customer.gift = False

        # overwrite coupon if another is used
        if coupon:
            customer.coupon = coupon
        customer.save()

        # save the memberships in the database
        helpers.new_account_memberships(supplement, has_paperback, video, customer, product_obj, product_obj2)

        # send success email to admin
        helpers.send_admin_charge_success_email(user.email, product_name, has_paperback, supplement, gifted_product)

        if not settings.DEBUG:
            # subscribe the person to convertkit
            helpers.subscribe_to_newsletter(user.email, product_slug, has_paperback)

            # invite the person into the slack channel
            helpers.invite_to_slack(user.email, product_name)

        # if this is a gifted product, send the person a gift email
        if 'giftee_user' in request.session:
            helpers.send_giftee_password_reset(
                request,
                user.email,
                product_name,
                'registration/giftee_password_reset_subject.txt',
                'registration/giftee_password_reset_email.txt',
                request.session.get('giftee_message'),
            )
            logout(request)
            messages.success(request, "Success! We've sent an email to your giftee with how to access their files.")
            request.session.pop('giftee_user', None)
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
        'product': product_slug,
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
