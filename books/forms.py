from django import forms

from django.contrib.auth.models import User

from books.widgets import NoNameTextInput


class EditEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Update your email address:"


class CardForm(forms.Form):
    last_4_digits = forms.CharField(required=True, min_length=4, max_length=4, widget=forms.HiddenInput())
    stripe_token = forms.CharField(required=True, widget=forms.HiddenInput())
    coupon = forms.CharField(required=False, widget=forms.HiddenInput())

    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


class StripePaymentForm(CardForm):
    card_number = forms.CharField(required=False, max_length=20, widget=NoNameTextInput(attrs={'class': 'card-number',}))
    card_cvc = forms.CharField(required=False, max_length=4,  widget=NoNameTextInput(attrs={'style':'width:80px'}))
    card_expiry_month = forms.CharField(required=False, max_length=2, widget=NoNameTextInput(attrs={'class': 'card-expiry-month','style':'width:63px'}))
    card_expiry_year = forms.CharField(required=False, max_length=4, widget=NoNameTextInput(attrs={'class': 'card-expiry-year','style':'width:76px'}))
    #card_address_zip = forms.CharField(required=False, max_length=10,  widget=NoNameTextInput(attrs={'style':'width:100px'}))
    coupon_code = forms.CharField(required=False, max_length=20,  widget=NoNameTextInput(attrs={'class': 'coupon-code',}))

    def __init__(self, *args, **kwargs):
        super(StripePaymentForm, self).__init__(*args, **kwargs)
        self.fields['card_number'].label = "Credit card number:"
        self.fields['card_number'].widget.attrs['autocompletetype'] = 'cc-number'
        self.fields['card_number'].widget.attrs['pattern'] = '\d*'
        self.fields['card_cvc'].label = "Credit card CVC:"
        self.fields['card_cvc'].widget.attrs['autocomplete'] = 'off'
        self.fields['card_cvc'].widget.attrs['autocompletetype'] = 'cc-csc'
        self.fields['card_cvc'].widget.attrs['pattern'] = '\d*'
        self.fields['card_expiry_month'].widget.attrs['placeholder'] = 'MM'
        self.fields['card_expiry_month'].widget.attrs['pattern'] = '\d*'
        self.fields['card_expiry_year'].widget.attrs['placeholder'] = 'YYYY'
        self.fields['card_expiry_year'].widget.attrs['pattern'] = '\d*'
        self.fields['coupon_code'].label = "Coupon code (optional):"

    def clean_card_number(self):
        if self.cleaned_data['card_number'] and (len(self.cleaned_data['card_number']) < 13 or len(self.cleaned_data['card_number']) > 16):
            raise forms.ValidationError("Please enter in a valid "+"credit card number.")
        return self.cleaned_data['card_number']
