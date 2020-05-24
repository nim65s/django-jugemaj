"""Templatetags for django-jugemaj."""
from django import template

from jugemaj.models import Vote

register = template.Library()


@register.filter
def vote(candidate, request):
    """Get (or create) the vote object for a connected user and a candidate."""
    try:
        return candidate.vote_set.get(elector=request.user).pk
    except Vote.DoesNotExist:
        return Vote.objects.create(elector=request.user, candidate=candidate).pk
