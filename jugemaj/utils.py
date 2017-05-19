from random import randint
from subprocess import check_output
from .models import Election, Candidate, Vote
from django.conf import settings

user_model = settings.AUTH_USER_MODEL


def randstr():
    return check_output(['pwgen', '8']).decode().strip()


def create_user(election=Election.objects.first()):
    user = User.objects.create(username=randstr(), password=randstr())
    for candidate in election.candidate_set.all():
        Vote.objects.create(elector_fk=user, candidate=candidate, choice=randint(1, 6))

