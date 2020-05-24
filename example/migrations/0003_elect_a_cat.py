# Generated by Django 3.0.6 on 2020-05-21 17:53

from datetime import timedelta

from django.db import migrations
from django.utils.timezone import now


def create_election(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Election = apps.get_model("jugemaj", "Election")
    Candidate = apps.get_model("jugemaj", "Candidate")
    ContentType = apps.get_model('contenttypes', 'ContentType')
    WikiDataModel = apps.get_model("example", "WikiDataModel")

    def content_type_and_object_id(obj):
        """Helper to get a content type & object id of an instance for use in migrations."""
        return {'object_id': obj.id, 'content_type': ContentType.objects.get_for_model(obj)}

    admin = User.objects.create(username='example_admin')
    election = Election.objects.create(name='Cats', creator=admin, end=now() + timedelta(days=365))

    for cat in WikiDataModel.objects.all():
        # In a migration, we need content_type & object_id.
        # But in usual code, this would be:
        # Candidate.objects.create(election=election, object=cat)
        Candidate.objects.create(election=election, **content_type_and_object_id(cat))


def delete_election(apps, schema_editor):
    User = apps.get_model("django.contrib.auth", "User")
    User.objects.get(username='example_admin').delete()  # Election & Candidate deleted by cascade


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('example', '0002_cats'),
        ('jugemaj', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_election, delete_election),
    ]
