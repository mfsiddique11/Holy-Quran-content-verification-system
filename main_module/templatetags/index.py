from django import template
register = template.Library()

@register.filter
def index(c, cl):
    return c[int(cl)]
