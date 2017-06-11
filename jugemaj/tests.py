from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Election, Candidate


class JugeMajTests(TestCase):
    def setUp(self):
        a, b, c = (User.objects.create_user(guy, email='%s@example.org' % guy, password=guy) for guy in 'abc')
        a.is_superuser = True
        a.save()

    def test_views(self):
        self.assertEqual(self.client.get(reverse('jugemaj:elections')).status_code, 200)
        self.assertEqual(self.client.get(reverse('jugemaj:create_election')).status_code, 302)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('jugemaj:create_election')).status_code, 200)
        r = self.client.post(reverse('jugemaj:create_election'), {
            'title': 'Élection du roi de Vénus',
            'description': 'Vénus n’a plus de roi, qui pensez-vous des candidats suivants ?',
            'end': '2025-03-09',
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Election.objects.count(), 1)
        slug = Election.objects.first().slug
        self.assertEqual(r.url, f'/election/{slug}/')
        self.assertEqual(self.client.get(r.url).status_code, 200)
        self.client.logout()
        self.assertEqual(self.client.get(r.url).status_code, 200)
        self.assertEqual(self.client.get(reverse('jugemaj:create_candidate', kwargs={'slug': slug})).status_code, 302)
        self.client.login(username='b', password='b')
        self.assertEqual(self.client.get(reverse('jugemaj:create_candidate', kwargs={'slug': slug})).status_code, 200)
        r = self.client.post(reverse('jugemaj:create_candidate', kwargs={'slug': slug}), {'name': 'Capitaine Zorg'})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, f'/election/{slug}/')
        self.assertEqual(Candidate.objects.count(), 1)
        for name in ['Buzz l’Éclair', 'Timon et Pumba', 'Sénateur Palpatine', 'Aragorn', 'Totoro']:
            Candidate.objects.create(name=name, election=Election.objects.first())
        self.client.logout()
        self.assertEqual(self.client.get(reverse('jugemaj:vote', kwargs={'slug': slug})).status_code, 302)
        self.client.login(username='b', password='b')
        self.assertEqual(self.client.get(reverse('jugemaj:vote', kwargs={'slug': slug})).status_code, 200)
        # r = self.client.post(reverse('jugemaj:vote', kwargs={'slug': slug}), { TODO })
