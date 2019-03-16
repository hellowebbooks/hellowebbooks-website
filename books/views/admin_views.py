from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html', {
    })
