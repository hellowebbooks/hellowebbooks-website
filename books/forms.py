from django import forms

from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User

from books.widgets import NoNameTextInput

# TODO: Might be good to update this later to update the username too so we aren't doing two database saves
class EditEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Update your email address"


class AddEmailForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(AddEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'buttercup@florin.com'
        self.fields['password'].widget.attrs['class'] = 'form-control'


    def clean_email(self):
        email = self.data['email']
        if "@" not in email:
            raise forms.ValidationError("Please enter a valid email address.")

        return email


class CardForm(forms.Form):
    last_4_digits = forms.CharField(required=True, min_length=4, max_length=4, widget=forms.HiddenInput())
    stripe_token = forms.CharField(required=True, widget=forms.HiddenInput())
    coupon = forms.CharField(required=False, widget=forms.HiddenInput())

    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class StripePaymentForm(CardForm):
    card_number = forms.CharField(required=False, max_length=20, widget=NoNameTextInput())
    card_cvc = forms.CharField(required=False, max_length=4,  widget=NoNameTextInput())
    card_expiry_month = forms.CharField(required=False, max_length=2, widget=NoNameTextInput())
    card_expiry_year = forms.CharField(required=False, max_length=4, widget=NoNameTextInput())
    #card_address_zip = forms.CharField(required=False, max_length=10,  widget=NoNameTextInput(attrs={'style':'width:100px'}))
    coupon_code = forms.CharField(required=False, max_length=20,  widget=NoNameTextInput())

    def __init__(self, *args, **kwargs):
        super(StripePaymentForm, self).__init__(*args, **kwargs)
        self.fields['card_number'].label = "Credit card number:"
        self.fields['card_number'].widget.attrs['autocompletetype'] = 'cc-number'
        self.fields['card_number'].widget.attrs['class'] = 'form-control card-number'
        self.fields['card_cvc'].label = "Credit card CVC:"
        self.fields['card_cvc'].widget.attrs['autocomplete'] = 'off'
        self.fields['card_cvc'].widget.attrs['autocompletetype'] = 'cc-csc'
        self.fields['card_cvc'].widget.attrs['pattern'] = '\d*'
        self.fields['card_cvc'].widget.attrs['class'] = 'form-control card-cvc'
        self.fields['card_cvc'].widget.attrs['style'] = 'display:inline-block;width:80px'
        self.fields['card_expiry_month'].widget.attrs['placeholder'] = 'MM'
        self.fields['card_expiry_month'].widget.attrs['pattern'] = '\d*'
        self.fields['card_expiry_month'].widget.attrs['class'] = 'form-control card-expiry-month'
        self.fields['card_expiry_month'].widget.attrs['style'] = 'display:inline-block;width:63px'
        self.fields['card_expiry_year'].widget.attrs['placeholder'] = 'YYYY'
        self.fields['card_expiry_year'].widget.attrs['pattern'] = '\d*'
        self.fields['card_expiry_year'].widget.attrs['class'] = 'form-control card-expiry-year'
        self.fields['card_expiry_year'].widget.attrs['style'] = 'display:inline-block;width:76px'
        self.fields['coupon_code'].label = "Coupon code (optional):"
        self.fields['coupon_code'].widget.attrs['class'] = 'form-control coupon-code'

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number'].replace("-","").replace(" ","")
        return card_number


class MyAuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Email"

    def clean_username(self):
        # use the email address to get the username for the account
        email = self.cleaned_data.get('username')
        username = email.replace("@", "").replace(".", "")
        return username


PRODUCTS = [
    ('ebook', 'eBook Only'),
    ('paperback', 'Paperback'),
    ('video', 'Video'),
]

class AdminAddCustomerForm(forms.Form):
    email = forms.EmailField()
    hello_web_app = forms.MultipleChoiceField(choices=PRODUCTS, widget=forms.CheckboxSelectMultiple(), required=False)
    hello_web_design = forms.MultipleChoiceField(choices=PRODUCTS, widget=forms.CheckboxSelectMultiple(), required=False)


class AdminAddCustomerBulkForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea)
    hello_web_app = forms.MultipleChoiceField(choices=PRODUCTS, widget=forms.CheckboxSelectMultiple(), required=False)
    hello_web_design = forms.MultipleChoiceField(choices=PRODUCTS, widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super(AdminAddCustomerBulkForm, self).__init__(*args, **kwargs)
        self.fields['emails'].label = "Comma delimited emails"


class ZineSignupForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ZineSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Add your email here to get access to the files"
        self.fields['email'].widget.attrs['placeholder'] = 'Your email address'
