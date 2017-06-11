from enum import IntEnum
from functools import cmp_to_key

from django.db import models
from django.conf import settings
from django.urls import reverse

from autoslug import AutoSlugField

CHOICES = IntEnum("choix", "Super Bien OK Passable Insuffisant Nul")


def enum_to_choices(enum):
    return ((item.value, item.name) for item in list(enum))


def sort_candidates(a, b):
    """
    a & b are the majority gauges of the candidates A & B:
    (p_A, α_A, q_A) & (p_B, α_B, q_B)
    where
    - α is the majority grade;
    - p the percentage of votes strictly above α;
    - q the percentage of votes strictly below α.
    thus, A > B ⇔ α_A > α_B || (α_A == α_B && (p_A > max(q_A, p_B, q_B) || q_B > max(p_A, q_A, p_B)))
    (eq. 2, p.11 of the second article in README.md)
    """
    a, b = a.majority_gauge(), b.majority_gauge()
    if a[1] > b[1]:
        return 1
    if b[1] > a[1]:
        return -1
    if a[0] > max(a[2], b[0], b[2]):
        return 1
    if b[0] > max(b[2], a[0], a[2]):
        return -1
    if b[2] > max(a[0], a[2], b[0]):
        return 1
    if a[2] > max(b[0], b[2], a[0]):
        return -1
    return 0


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
        return sorted(self.candidate_set.all(), key=cmp_to_key(sort_candidates))


class Candidate(TimeStampedModel):
    name = models.CharField("nom", max_length=250)
    election = models.ForeignKey(Election)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.election.get_absolute_url()

    def majority_gauge(self):
        count = self.vote_set.count()
        if not count:
            return (0, 10, 0)
        mention = self.vote_set.order_by('choice')[count // 2].choice
        return (self.vote_set.filter(choice__gt=mention).count() / count, mention,
                self.vote_set.filter(choice__lt=mention).count() / count)

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
