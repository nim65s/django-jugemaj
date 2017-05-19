from enum import IntEnum
from math import floor

from django.db import models
from django.conf import settings
from django.urls import reverse

from autoslug import AutoSlugField

CHOICES = IntEnum("choix", "Super Bien OK Passable Insuffisant Nul")


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


class Election(models.Model):
    title = models.CharField("titre", max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField("fini", default=False)
    end = models.DateTimeField("fin")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jugemaj:election', kwargs={'slug': self.slug})

    def results(self):
        return sorted([candidate.votes() for candidate in self.candidate_set.all()])


class Candidate(models.Model):
    name = models.CharField("nom", max_length=250)
    election = models.ForeignKey(Election)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.election.get_absolute_url()

    def votes(self):
        count = self.vote_set.count()
        if count:
            mention = self.vote_set.order_by('choice')[min(floor(count / 2), count - 1)].choice
            return mention, count, [self.vote_set.filter(choice=i).count() * 100 / count for i in CHOICES], self.name
        return 0, 0, [], self.name


class Vote(models.Model):
    elector_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    elector_name = models.CharField("votre nom", max_length=250, null=True)
    candidate = models.ForeignKey(Candidate)
    choice = models.IntegerField("choix", choices=enum_to_choices(CHOICES), null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def elector(self):
        return self.elector_name or str(self.elector_fk)

    def __str__(self):
        return f"vote de {self.elector} pour {self.candidate}"

    class Meta:
        ordering = ('created',)
