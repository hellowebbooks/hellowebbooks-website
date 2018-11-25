from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    success_url = 'dashboard'
