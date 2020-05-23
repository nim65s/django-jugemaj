"""Django models for the example app."""

from django.db import models

from wikidata.client import Client  # type: ignore

LANGS = ['fr', 'en']  # ordered list of langages to check on wikidata


class WikiDataModel(models.Model):
    """A django model to represent something available on wikidata."""
    name = models.CharField(max_length=50, blank=True)
    wikidata = models.PositiveIntegerField()

    def __str__(self):
        """Get the name of this wikidata instance."""
        return self.name

    @property
    def wikidata_url(self):
        """Get a direct link to the wikidata item."""
        return f'https://www.wikidata.org/wiki/Q{self.wikidata}'

    def update_name(self):
        """Update the name from wikidata."""
        labels = Client().get(f'Q{self.wikidata}', load=True).data['labels']
        self.name = next(labels[lang] for lang in LANGS if lang in labels)['value']
        self.save()
