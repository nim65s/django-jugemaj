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
        results = sorted([candidate.votes() for candidate in self.candidate_set.all()])
        lsts = self.results_split(results)
        print('first', {l[0][0]: len(l) for l in lsts})
        lsts = [self.results_split(sorted([item[-1].votes(exclude=lst[0][0]) for item in lst]))
                if len(lst) != 1 else lst for lst in lsts]
        print('last', lsts)
        return results

    def results_split(self, results):
        mention = -1
        lsts = []
        for result in results:
            if mention != result[0]:
                lsts.append([])
                mention = result[0]
            lsts[-1].append(result)
        return lsts


class Candidate(models.Model):
    name = models.CharField("nom", max_length=250)
    election = models.ForeignKey(Election)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.election.get_absolute_url()

    def votes(self, exclude=None):
        count = self.vote_set.exclude(choice=exclude).count()
        if count:
            mention = self.vote_set.exclude(choice=exclude).order_by('choice')[min(floor(count / 2), count - 1)].choice
            return mention, count, [self.vote_set.filter(choice=i).count() * 100 / count for i in CHOICES], self
        return 0, 0, [], self


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
