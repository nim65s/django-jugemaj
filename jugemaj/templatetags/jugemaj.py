from django import template

from jugemaj.models import CHOICES

register = template.Library()


@register.filter
def candidate(candidate, candidates):
    return candidates[candidate]


@register.filter
def mentions(candidate):
    return ', '.join(CHOICES(mention).name for mention in candidate.mentions())
