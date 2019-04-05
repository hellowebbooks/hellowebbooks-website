import os
import stripe

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from books import forms, options, helpers
from books.models import Product, Membership, Customer


@login_required
def dashboard(request):
    try:
        customer = Customer.objects.get(user=request.user)
        memberships = Membership.objects.filter(customer=customer)
    except ObjectDoesNotExist:
        messages.error(request, 'Customer not found. If this is in error, please email tracy@hellowebbooks.com with details.')
        return redirect('order')

    # if someone has no memberships, means they went through the create account
    # page but didn't buy a product. Redirect to charge.
    if len(memberships) == 0:
        messages.info(request, 'You will get access to the dashboard after ordering a product. :)')
        return redirect('order')

    membership_list = [m.product.name for m in memberships]

    return render(request, 'dashboard/dashboard.html', {
        'customer': customer,
        'memberships': memberships,
        'membership_list': membership_list,
        'dashboard_area': True,
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
def course(request, product_slug, link=None):
    product_name = product_slug.replace("-", " ")
    product = Product.objects.get(name__iexact=product_name)
    course = options.course_list[product.name]

    try:
        membership = Membership.objects.get(
            customer__user=request.user,
            product__name=product.name,
        )
    except ObjectDoesNotExist:
        messages.error(request, 'Membership not found. If this is in error, please email tracy@hellowebbooks.com with details.')
        return redirect('order')

    # if default page, then show the last read page or the intro page
    if not link:
        link = 'intro'
        if membership.last_read:
            link = membership.last_read

    membership.last_read = link
    membership.save()

    # loop through options to get details for this course
    video_url, course_name, course_template, course_link, prev_link, prev_name, next_link, next_name = helpers.get_course_info(course, link)

    return render(request, "dashboard/course/course.html", {
        'product': product,
        'membership': membership,
        'course': course,
        'course_template': course_template,
        'course_name': course_name,
        'course_link': course_link,
        'video_url': video_url,
        'prev_link': prev_link,
        'prev_name': prev_name,
        'next_link': next_link,
        'next_name': next_name,
        'dashboard_area': True,
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
def edit_email(request):
    user = request.user
    form_class = forms.EditEmailForm

    if request.method == 'POST':
        org_email = user.email
        form = form_class(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            # TODO: Might be good to update this later to update the username
            # too so we aren't doing two database saves with the below

            # update their "username" accordingly
            email = user.email
            username = email.replace("@", "").replace(".", "")
            user.username = username
            user.save()

            # update their email address in stripe too
            customer = Customer.objects.get(user=user)

            if customer.stripe_id: # so this doesn't include gifted/imported folks
                stripe.Customer.modify(
                    customer.stripe_id,
                    email=user.email,
                    description=user.username,
                )

            messages.success(request, 'Your email address has been updated!')
            return redirect('dashboard')

    else:
        form = form_class(instance=user)

    return render(request, 'dashboard/edit_email.html', {
        'form': form,
        'dashboard_area': True,
    })


@login_required
def add_product(request, product_slug):
    try:
        customer = Customer.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, 'Customer not found. If this is in error, please email tracy@hellowebbooks.com with details.')
        return redirect('order')

    product_name = product_slug.replace("-", " ")
    if 'really friendly' not in product_name:
        messages.error(request, 'Cannot add that product, sorry!')
        return redirect('dashboard')

    product_obj = Product.objects.get(name__iexact=product_name)
    membership = Membership(
        customer = customer,
        product = product_obj,
        paperback = False,
        video = True,
    )
    membership.save()

    messages.success(request, 'Product has been added to your account!')
    return redirect('dashboard')
