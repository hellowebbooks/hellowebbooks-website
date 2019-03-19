import os
import stripe
import requests

from django.contrib import messages
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


def create_stripe_customer(request, product_slug, user, source, shipping, coupon):
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
        return redirect('charge', product_slug=product_slug)
    except stripe.error.StripeError as e:
        body = e.json_body
        err  = body.get('error', {})
        if err.get('param') == 'coupon':
            messages.error(request, 'Sorry, that coupon is invalid!')
        else:
            messages.error(request, "Sorry, an error has occured! We've been emailed this issue and will be on it within 24 hours. If you'd like to know when we've fixed it, email tracy@hellowebbooks.com. Our sincere apologies.")
            mail_admins("Bad happenings on HWB", "Payment failure for [%s] - [%s]" % (user.email, e))
        return redirect('charge', product_slug=product_slug)

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
    # FIXME: Price would be nice here too
    # TODO: This is a silly way to do things, make this better.
    content = '%s bought %s. Supplement: %s. Shipping: %s. Gifted? %s' % (user_email, product_name, supplement, has_paperback, gifted_product)

    # send email to admin
    send_mail(
        'New payment on Hello Web Books',
        content,
        'noreply@hellowebbooks.com',
        ['tracy@hellowebbooks.com'],
    )


def send_giftee_password_reset(request, email, product_name, subject_template_name, email_template_name, giftee_message=None):
    form = PasswordResetForm({'email': email})
    assert form.is_valid()
    form.save(
        request=request,
        from_email="Tracy Osborn <tracy@hellowebbooks.com>",
        subject_template_name=subject_template_name,
        email_template_name=email_template_name,
        extra_email_context={ 'product': product_name, 'message': giftee_message },
    )
    request.session.pop('giftee_user', None)
    request.session.pop('giftee_message', None)


def get_course_info(course, link):
    video_url = ""
    course_name = ""
    course_template = ""
    prev_link = ""
    prev_name = ""
    next_link = ""
    next_name = ""
    info_hit = False
    stop_loop = False
    once_more = False

    # loop through course
    module_count = 0
    module_total = len(course)
    for k, v in course.items():
        total = len(v)
        module_count +=1
        count = 0
        # loop through module
        for key, value in v.items():
            count += 1
            if info_hit:
                next_link = value['link']
                next_name = value['name']
                return video_url, course_name, course_template, prev_link, prev_name, next_link, next_name

            if value['link'] != link:
                prev_link = value['link']
                prev_name = value['name']
                continue

            video_url = value['video']
            course_name = value['name']
            course_template = "dashboard/" + value['template']
            info_hit = True

            # if we're at the end of the loop, return early without filling out next
            if count == total and course_name:
                stop_loop = True
                break

        # we should only get here if we returned early in the inner loop
        if stop_loop and not once_more:
            if module_count == module_total:
                return video_url, course_name, course_template, prev_link, prev_name, next_link, next_name
            once_more = True
            continue

        if stop_loop and once_more:
            return video_url, course_name, course_template, prev_link, prev_name, next_link, next_name


def subscribe_to_newsletter(email, product_slug, has_paperback):
    convertkit_secret = os.environ['CONVERTKIT_SECRET']
    convertkit_public = os.environ['CONVERTKIT_PUBLIC']
    convertkit_form_id = 874212 # the dummy form we're subscribing them to in convertkit

    # this isn't used, it's for reference for the redonkulous if/else statement
    CONVERTKIT_TAG_LOOKUP = {
        'From: Website': '824915',
        'Own: HWA': '330744',
        'Own: HWA eBook': '330767',
        'Own: HWA Paperback': '330768',
        'Own: HWA Videos': '330769',
        'Own: HWAIC': '330745',
        'Own: HWAIC eBook': '330770',
        'Own: HWAIC Paperback': '330776',
        'Own: HWAIC Videos': '330771',
        'Own: HWD': '330747',
        'Own: HWD eBook': '330764',
        'Own: HWD Paperback': '330765',
        'Own: HWD Videos': '330766',
    }

    # by default, adding the "From: Website" tag
    tags = ['824915',]

    # FIXME: There *must* be a better way to do this. Fix me later.
    if product_slug == 'hwb-video' and has_paperback:
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330747') # Own: HWD
        tags.append('330769') # Own: HWA Videos
        tags.append('330771') # Own: HWAIC Videos
        tags.append('330766') # Own: HWD Videos
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwb-video':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330747') # Own: HWD
        tags.append('330769') # Own: HWA Videos
        tags.append('330771') # Own: HWAIC Videos
        tags.append('330766') # Own: HWD Videos
    elif product_slug == 'hwb-pb':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330747') # Own: HWD
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwb-ebooks' and has_paperback:
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330747') # Own: HWD
        tags.append('330767') # Own: HWA eBook
        tags.append('330770') # Own: HWAIC eBook
        tags.append('330764') # Own: HWD eBook
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwb-ebooks':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330747') # Own: HWD
        tags.append('330767') # Own: HWA eBook
        tags.append('330770') # Own: HWAIC eBook
        tags.append('330764') # Own: HWD eBook
    elif product_slug == 'hwa-video' and has_paperback:
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330769') # Own: HWA Videos
        tags.append('330771') # Own: HWAIC Videos
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
    elif product_slug == 'hwa-video':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330769') # Own: HWA Videos
        tags.append('330771') # Own: HWAIC Videos
    elif product_slug == 'hwa-pb':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
    elif product_slug == 'hwa-ebooks' and has_paperback:
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330767') # Own: HWA eBook
        tags.append('330770') # Own: HWAIC eBook
        tags.append('330768') # Own: HWA Paperback
        tags.append('330776') # Own: HWAIC Paperback
    elif product_slug == 'hwa-ebooks':
        tags.append('330744') # Own: HWA
        tags.append('330745') # Own: HWAIC
        tags.append('330767') # Own: HWA eBook
        tags.append('330770') # Own: HWAIC eBook
    elif product_slug == 'hwd-video' and has_paperback:
        tags.append('330747') # Own: HWD
        tags.append('330766') # Own: HWD Videos
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwd-video':
        tags.append('330747') # Own: HWD
        tags.append('330766') # Own: HWD Videos
    elif product_slug == 'hwd-pb':
        tags.append('330747') # Own: HWD
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwd-ebooks' and has_paperback:
        tags.append('330747') # Own: HWD
        tags.append('330764') # Own: HWD eBook
        tags.append('330765') # Own: HWD Paperback
    elif product_slug == 'hwd-ebooks':
        tags.append('330747') # Own: HWD
        tags.append('330764') # Own: HWD eBook
    elif product_slug == 'hwa-video-supplement':
        tags.append('330769') # Own: HWA Videos
    elif product_slug == 'hwd-video-supplement':
        tags.append('330766') # Own: HWD Videos

    # convert to comma delimited string for convertkit
    tag_string = ','.join(map(str, tags))

    # make api call
    url = 'https://api.convertkit.com/v3/forms/%d/subscribe' % convertkit_form_id
    payload = {'api_key': convertkit_public, 'email': email, 'tags': tag_string}
    r = requests.post(url, params=payload)
    if r.status_code != 200:
        mail_admins("Subscribe to Convertkit failed (%d)" % r.status_code, "Subscribe failure for [%s], product: [%s]" % (email, product_slug))
    return
