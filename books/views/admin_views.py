from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from books import helpers
from books.models import Customer, Product, Membership
from books.forms import AdminAddCustomerForm


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    customer_count = Customer.objects.count()
    return render(request, 'admin/dashboard.html', {
        'customer_count': customer_count,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_add_customer(request):
    form_class = AdminAddCustomerForm
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            hello_web_app = form.cleaned_data['hello_web_app']
            hello_web_design = form.cleaned_data['hello_web_design']

            # check to make sure they're not already in system
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email address found in system')
                return redirect('admin_add_customer')

            # create user
            user = User.objects.create_user(
                username=email.replace("@", "").replace(".", ""),
                email=email,
                password=User.objects.make_random_password(),
            )

            # create Customer from user
            customer = Customer.objects.create(user=user)

            # make appropriate Memberships based on form
            if hello_web_app:
                hwa_product_obj = Product.objects.get(name="Hello Web App")
                paperback = False
                if 'paperback' in hello_web_app:
                    paperback = True
                video = False
                if 'video' in hello_web_app:
                    video = True
                Membership.objects.create(
                    customer=customer,
                    product=hwa_product_obj,
                    paperback=paperback,
                    video=video,
                )

            if hello_web_design:
                hwd_product_obj = Product.objects.get(name="Hello Web Design")
                paperback = False
                if 'paperback' in hello_web_design:
                    paperback = True
                video = False
                if 'video' in hello_web_design:
                    video = True
                Membership.objects.create(
                    customer=customer,
                    product=hwd_product_obj,
                    paperback=paperback,
                    video=video,
                )

            # send User an email with how to access and reset the password
            helpers.send_giftee_password_reset(
                request,
                user.email,
                "Admin Add",
                'registration/admin_add_password_reset_subject.txt',
                'registration/admin_add_password_reset_email.txt',
            )

            # refresh page with success
            messages.success(request, 'Customer has been added!')
            return redirect('admin_add_customer')
    else:
        form = form_class()

    return render(request, 'admin/add_customer.html', {
        'form': form,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_export_customer_emails(request):
    customers = Customer.objects.all()
    return render(request, 'admin/export-emails.html', {
        'customers': customers,
    })
