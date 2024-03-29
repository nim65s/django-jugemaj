"""Django models for the jugemaj app."""
from functools import cmp_to_key

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from ndh.models import NamedModel, TimeStampedModel

# ref https://github.com/typeddjango/django-stubs/issues/729
CHOICES = models.IntegerChoices("choix", "Super Bien OK Passable Insuffisant Nul")  # type: ignore


def sort_candidates(a, b):
    """
    Sort candidates a & b by their majority gauge.

    - α is the majority grade;
    - p the percentage of votes strictly above α;
    - q the percentage of votes strictly below α.

    a > b ⇔ a_α > b_α || (a_α == b_α && (a_p > max(a_q, b_p, b_q) || b_q > max(a_p, a_q, b_p)))

    (ref eq. 2, p.11 of the second article in README.md)
    """
    (a_p, a_α, a_q), (b_p, b_α, b_q) = a.majority_gauge(), b.majority_gauge()
    if a_α > b_α:
        return 1
    if b_α > a_α:
        return -1
    if a_p > max(a_q, b_p, b_q):
        return 1
    if b_p > max(b_q, a_p, a_q):
        return -1
    if b_q > max(a_p, a_q, b_p):
        return 1
    if a_q > max(b_p, b_q, a_p):
        return -1
    return 0


class Election(NamedModel, TimeStampedModel):
    """Main model for the jugemaj app."""

    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    end = models.DateTimeField("fin")
    ended = models.BooleanField("fini", default=False)

    def get_absolute_url(self):
        """Reverse to the detail view for this instance."""
        return reverse("jugemaj:election", kwargs={"slug": self.slug})

    def results(self):
        """Get the sorted list of all Candidates for this Election."""
        return sorted(self.candidate_set.all(), key=cmp_to_key(sort_candidates))


class Candidate(models.Model):
    """An Election as Candidate as choices."""

    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        """Print the candidate."""
        return str(self.content_object)

    def get_absolute_url(self):
        """Get the candidate's Election URL."""
        return self.election.get_absolute_url()

    def majority_gauge(self):
        """Compute the majority gauge of this Candidate."""
        count = self.vote_set.count()
        if not count:
            return (0, 10, 0)
        mention = self.vote_set.order_by("choice")[count // 2].choice
        if mention is None:
            mention = 6
        return (
            self.vote_set.filter(choice__gt=mention).count() / count,
            mention,
            self.vote_set.filter(choice__lt=mention).count() / count,
        )

    def votes(self):
        """Get the list of the votes for this Candidate."""
        count = self.vote_set.count()
        if count:
            return [
                self.vote_set.filter(choice=i).count() * 100 / count for i in CHOICES
            ]
        return [0] * len(CHOICES)


class NamedCandidate(NamedModel, TimeStampedModel):
    """A common model to be used as a Candidate object."""

    candidates = GenericRelation(Candidate)


class Vote(TimeStampedModel):
    """In an Election, each elector can give a rating to each Candidate."""

    elector = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    choice = models.IntegerField("choix", choices=CHOICES.choices, null=True)

    class Meta:
        """An elector has only one rating on each Candidate."""

        unique_together = ("elector", "candidate")

    def __str__(self):
        """Describe an elector rating."""
        return f"vote de {self.elector} pour {self.candidate}: {self.choice}"

    def get_absolute_url(self):
        """Let an elector a choice for a candidate."""
        return reverse("jugemaj:vote", kwargs={"pk": self.pk})
