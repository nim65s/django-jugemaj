# Django Jugemaj

```eval_rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   reference
   foot
```

An app that define Election and Candidate models, and implements a Jugement
Majoritaire on those.

Any model can be a Candidate, thanks to [Generic Foreign
Keys](https://docs.djangoproject.com/en/3.0/ref/contrib/contenttypes/).


## Example

This app comes with a `testproject` django project to run tests, and an
`example` app to showcase how to use the `jugemaj` app.


So let's start by creating one model. Let's say we want a list of cats from
wikidata.

We need to define the model:


```eval_rst
.. literalinclude:: ../example/models.py
   :language: python
   :lines: 10-13
```

And to populate it:

```eval_rst
.. literalinclude:: ../example/migrations/0002_cats.py
   :language: python
   :lines: 19-24
   :dedent: 4
```

Next, we can create an Election instance

```eval_rst
.. literalinclude:: ../example/migrations/0003_elect_a_cat.py
   :language: python
   :lines: 20-22
   :dedent: 4
```

And declare our cats as candidates for it:

```eval_rst
.. literalinclude:: ../example/migrations/0003_elect_a_cat.py
   :language: python
   :lines: 24-28
   :dedent: 4
```
