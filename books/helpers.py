import os
import stripe

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, mail_admins
from django.shortcuts import redirect

from books import options
from books.models import Product, Membership

stripe.api_key = os.environ['STRIPE_SECRET']


def product_details(product):
    try:
        amount = options.PRODUCT_LOOKUP[product].amount or 0
        product_name = options.PRODUCT_LOOKUP[product].description or ""
        us_postage = options.PRODUCT_LOOKUP[product].us_postage or 0
        can_postage = options.PRODUCT_LOOKUP[product].can_postage or 0
        aus_postage = options.PRODUCT_LOOKUP[product].aus_postage or 0
        eur_postage = options.PRODUCT_LOOKUP[product].eur_postage or 0
        else_postage = options.PRODUCT_LOOKUP[product].else_postage or 0
        paperback_price = options.PRODUCT_LOOKUP[product].paperback_addl or 0
    except KeyError:
        messages.error(request, "Product not found.")
        mail_admins("Bad happenings on HWB", "Product not found in order page: [%s]" % (product))
        return redirect('order')

    return amount, product_name, us_postage, can_postage, aus_postage, eur_postage, else_postage, paperback_price


# TODO: This is probably a dumb way of doing this. Look into something
# more future-proof.
def product_split(product):
    paperback = False
    video = False
    supplement = False
    product_obj2 = None

    split_product = product.split("-")
    if split_product[0] == "hwa":
        product_obj = Product.objects.get(name="Hello Web App")
    elif split_product[0] == "hwd":
        product_obj = Product.objects.get(name="Hello Web Design")
    elif split_product[0] == "hwb":
        hwb_bundle = True
        product_obj = Product.objects.get(name="Hello Web App")
        product_obj2 = Product.objects.get(name="Hello Web Design")

    if split_product[1] == "pb":
        paperback = True

    if split_product[1] == "video":
        video = True

    if len(split_product) == 3:  # three arguments means it's an update to pkg
        supplement = True

    return product_obj, product_obj2, paperback, video, supplement


def shipping_details(args):
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

    return shipping


def create_stripe_customer(product, user, source, shipping, coupon):
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

    return id


def create_memberships(supplement, has_paperback, video, customer, product_obj, product_obj2):
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
        membership = Membership(
            customer = customer,
            product = product_obj,
            paperback = has_paperback, # set from form after if statement
            video = video, # set before POST if statement
        )
        membership.save()

        if product_obj2:
            membership2 = Membership(
                customer = customer,
                product = product_obj2,
                paperback = has_paperback, # set from form after if statement
                video = video, # set before POST if statement
            )
            membership2.save()


def send_admin_charge_success_email(user_email, product_name, has_paperback, supplement, gifted_product):
    # FIXME: Need to pass along shipping details too
    # TODO: This is a silly way to do things, make this better.
    content = '%s bought %s. Supplement: %s. Shipping: %s. Gifted? %s' % (user_email, product_name, supplement, has_paperback, gifted_product)

    # send email to admin
    send_mail(
        'New payment on Hello Web Books',
        content,
        'noreply@hellowebbooks.com',
        ['tracy@hellowebbooks.com'],
    )


def send_giftee_password_reset(request, email, product_name, giftee_message):
    form = PasswordResetForm({'email': email})
    assert form.is_valid()
    # XXX: Test that empty messages work
    form.save(
        request=request,
        from_email="tracy@hellowebbooks.com",
        subject_template_name='registration/giftee_password_reset_subject.txt',
        email_template_name='registration/giftee_password_reset_email.txt',
        extra_email_context={ 'product': product_name, 'message': giftee_message },
    )
    logout(request)
    request.session.pop('giftee_user', None)
    request.session.pop('giftee_message', None)


def get_video_info_from_course(course, link):
    video_url = ""
    video_name = ""
    video_template = ""
    prev_link = ""
    prev_name = ""
    next_link = ""
    next_name = ""
    info_hit = False

    for key, value in course.items():
        total = len(value)
        count = 0
        for key, value in value.items():
            count += 1
            if info_hit:
                next_link = value['link']
                next_name = value['name']
                return video_url, video_name, video_template, prev_link, prev_name, next_link, next_name

            if value['link'] != link:
                prev_link = value['link']
                prev_name = value['name']
                continue

            video_url = value['video']
            video_name = value['name']
            video_template = "dashboard/" + value['template']
            info_hit = True

            # if we're at the end of the loop, return early without filling out next
            if count == total and video_name:
                return video_url, video_name, video_template, prev_link, prev_name, next_link, next_name
