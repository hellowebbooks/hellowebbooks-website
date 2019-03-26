from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from books.models import Customer, Membership, Product


UserAdmin.list_display = ('email', 'date_joined', 'is_staff')


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('user_email', 'stripe_id', 'last_4_digits', 'coupon', 'gift',)
    search_fields = ('user__email', 'stripe_id', 'coupon',)
    inlines = [MembershipInline,]


class MembershipAdmin(admin.ModelAdmin):
    model = Membership
    list_display = ('customer', 'product', 'paperback', 'video',)
    search_fields = ('customer__user__email',)


class ProductAdmin(admin.ModelAdmin):
    model = Product


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Product, ProductAdmin)
