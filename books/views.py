from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from books import forms
from books.models import Product, Membership
from blog.models import PostPage


def index(request):
    posts = PostPage.objects.select_related().all()
    return render(request, 'index.html', {
        'posts': posts,
    })


def order(request):
    # XXX: Probably want to remove the below and
    # keep the order stuff to manual listings for now.
    products = Product.objects.all()
    return render(request, 'order.html', {
        'products': products,
    })


@login_required
def dashboard(request):
    memberships = Membership.objects.filter(customer__user=request.user)
    return render(request, 'dashboard/dashboard.html', {
        'memberships': memberships,
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
