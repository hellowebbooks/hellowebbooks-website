from django import template
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def markdown(value, arg=''):
    try:
        import commonmark
    except ImportError:
        logging.warning("Markdown package not installed.")
        return force_text(value)
    else:
        parser = commonmark.Parser()
        ast = parser.parse(value)
        renderer = commonmark.HtmlRenderer()
        html = renderer.render(ast)
        return mark_safe(html)
