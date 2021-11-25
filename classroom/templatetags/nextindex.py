from django import template
register = template.Library()

@register.filter
def nextindex(indexable, i):
    return indexable[i+1]