from django import template

register = template.Library()


@register.filter
def candidate(candidate, candidates):
    return candidates.get(candidate)
