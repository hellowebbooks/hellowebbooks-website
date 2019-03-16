from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from books.models import Customer


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    customer_count = Customer.objects.count()
    return render(request, 'admin/dashboard.html', {
        'customer_count': customer_count,
    })
