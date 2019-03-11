from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(Timestamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name="customers")
    stripe_id = models.CharField(max_length=255, blank=True)
    last_4_digits = models.CharField(max_length=255, blank=True)
    coupon = models.CharField(max_length=255, blank=True)
    gift = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user.email


# FIXME: Hm, I may want a slugfield here
class Product(models.Model):
    name = models.CharField(max_length=50)
    customers = models.ManyToManyField(Customer, through='Membership')

    def __str__(self):
        return self.name

    def get_slug(self):
        return slugify(self.name)


class Membership(Timestamp):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
        related_name="customers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
        related_name="products")
    paperback = models.BooleanField(default=False)
    video = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.user.username
