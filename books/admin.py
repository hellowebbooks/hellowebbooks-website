from django.contrib import admin

from books.models import Customer, Membership, Product


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('user_email', 'stripe_id', 'last_4_digits', 'coupon', 'gift',)
    search_fields = ('user__email', 'stripe_id', 'coupon',)

class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('customer', 'product', 'paperback', 'video',)
    search_fields = ('customer__user__email',)

class ProductAdmin(admin.ModelAdmin):
    model = Product


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Product, ProductAdmin)
