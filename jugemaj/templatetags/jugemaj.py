from django import template

from jugemaj.models import CHOICES

register = template.Library()


@register.filter
def candidate(candidate, candidates):
    return candidates[candidate]


@register.filter
def choices(mention):
    return CHOICES(mention).name
