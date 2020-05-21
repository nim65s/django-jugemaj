"""Django models for the example app."""

from django.db import models

from ndh.models import Links
from wikidata.client import Client

LANGS = ['fr', 'en']  # ordered list of langages to check on wikidata


class WikiDataModel(models.Model, Links):
    """
    A django model to represent something available on wikidata.

    This is populated with a list of cats in the second migration.
    """
    label = models.CharField(max_length=50, blank=True)
    wikidata = models.PositiveIntegerField()

    def __str__(self):
        """Get the label of this wikidata instance."""
        return self.label

    @property
    def wikidata_url(self):
        """Get a direct link to the wikidata item."""
        return f'https://www.wikidata.org/wiki/Q{self.wikidata}'

    def update_label(self):
        """Update the label from wikidata."""
        labels = Client().get(f'Q{self.wikidata}', load=True).data['labels']
        self.label = next(labels[lang] for lang in LANGS if lang in labels)['value']
        self.save()
