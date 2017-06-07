from enum import IntEnum
from math import floor

from django.db import models
from django.conf import settings
from django.urls import reverse

from autoslug import AutoSlugField

CHOICES = IntEnum("choix", "Super Bien OK Passable Insuffisant Nul")


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Election(TimeStampedModel):
    title = models.CharField("titre", max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    end = models.DateTimeField("fin")
    ended = models.BooleanField("fini", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jugemaj:election', kwargs={'slug': self.slug})

    def results(self):
        return sorted(self.candidate_set.all(), key=lambda c: c.mentions())


class Candidate(TimeStampedModel):
    name = models.CharField("nom", max_length=250)
    election = models.ForeignKey(Election)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.election.get_absolute_url()

    def mentions(self, exclude=None):
        if exclude is None:
            exclude = []
        votes = self.vote_set.exclude(choice__in=exclude)
        count = votes.count()
        if not count:
            return []
        mention = [votes.order_by('choice')[count // 2].choice]
        return mention + self.mentions(exclude=exclude + mention)

    def votes(self):
        count = self.vote_set.count()
        if count:
            return [self.vote_set.filter(choice=i).count() * 100 / count for i in CHOICES]
        return [0] * len(CHOICES)


class Vote(TimeStampedModel):
    elector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate)
    choice = models.IntegerField("choix", choices=enum_to_choices(CHOICES), null=True)

    class Meta:
        unique_together = ('elector', 'candidate')

    def __str__(self):
        return f"vote de {self.elector} pour {self.candidate}: {self.choice}"
