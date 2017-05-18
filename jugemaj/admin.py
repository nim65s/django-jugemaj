from django.contrib.admin import site

from .models import Election, Candidate, Vote

for model in [Election, Candidate, Vote]:
    site.register(model)
