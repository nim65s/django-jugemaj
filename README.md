# Jugement Majoritaire

[![Documentation Status](https://readthedocs.org/projects/django-jugemaj/badge/?version=latest)](https://django-jugemaj.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/django-jugemaj.svg)](https://pypi.org/project/django-jugemaj)
[![Tests](https://github.com/nim65s/django-jugemaj/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/django-jugemaj/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/django-jugemaj/master.svg)](https://results.pre-commit.ci/latest/github/nim65s/django-jugemaj/master)
[![codecov](https://codecov.io/gh/nim65s/django-jugemaj/branch/master/graph/badge.svg?token=Z5AEN8BA0F)](https://codecov.io/gh/nim65s/django-jugemaj)
[![Maintainability](https://api.codeclimate.com/v1/badges/6737a84239590ddc0d1e/maintainability)](https://codeclimate.com/github/nim65s/django-jugemaj/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Application de vote par [Jugement Majoritaire](https://fr.wikipedia.org/wiki/Jugement_majoritaire).

## Requirements

- [ndh](https://pypi.python.org/pypi/ndh)
    - [django](https://www.djangoproject.com/)
    - [django-autoslug](https://github.com/justinmayer/django-autoslug/)
    - [django-bootstrap5](https://github.com/zostera/django-bootstrap5) (can be made optional on request))

Tested with:
- Python 3.8, 3.9
- [Django](https://www.djangoproject.com/) 2.2+

## Theory

- [A theory of measuring, electing, and ranking. *Michel Balinski and Rida Laraki*. In PNAS 2007](https://doi.org/10.1073/pnas.0702634104)
- [Majority judgement vs. majority rule. *Michel Balinski and Rida Laraki*. In Social Choice and Welfare 2016](https://hal.archives-ouvertes.fr/hal-02374645)
