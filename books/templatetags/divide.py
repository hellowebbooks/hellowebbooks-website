from django import template

register = template.Library()
@register.filter
def cents_to_dollars(cents):
    int_cents = int(float(cents))
    return '{:0.2f}'.format(int_cents/100.0)
