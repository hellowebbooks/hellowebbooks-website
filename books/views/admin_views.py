from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from books import helpers, forms
from books.models import Customer, Product, Membership


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    customer_count = Customer.objects.count()
    return render(request, 'admin/dashboard.html', {
        'customer_count': customer_count,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_add_customer(request):
    form_class = forms.AdminAddCustomerForm
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

            # create User, Customer, and Membership objects
            helpers.manual_admin_add_customer(request, email, hello_web_app, hello_web_design)

            # refresh page with success
            messages.success(request, 'Customer has been added!')
            return redirect('admin_add_customer')
    else:
        form = form_class()

    return render(request, 'admin/add_customer.html', {
        'form': form,
    })


@user_passes_test(lambda u: u.is_staff)
def admin_add_customer_bulk(request):
    form_class = forms.AdminAddCustomerBulkForm
    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            # XXX: Update this to loop around what emails were added
            emails = form.cleaned_data['emails']
            hello_web_app = form.cleaned_data['hello_web_app']
            hello_web_design = form.cleaned_data['hello_web_design']

            email_list = [item.strip() for item in emails.split(',')]
            pass_list = []

            for email in email_list:
                # check to make sure they're not already in system
                if User.objects.filter(email=email).exists():
                    print("no gusta " + email)
                    pass_list.append(email)
                    continue

                # create User, Customer, and Membership objects
                helpers.manual_admin_add_customer(request, email, hello_web_app, hello_web_design)

            # refresh page with success
            messages.success(request, 'Customers have been added! Skipped %s' % pass_list)
            return redirect('admin_add_customer_bulk')
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
