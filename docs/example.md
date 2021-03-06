## Example

This app comes with a `testproject` django project to run tests, and an
`example` app to showcase how to use the `jugemaj` app. We'll show here
some parts extracted from the `example` app.


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
   :lines: 21-24
   :dedent: 4
```

Next, we can create an Election instance

```eval_rst
.. literalinclude:: ../example/migrations/0003_elect_a_cat.py
   :language: python
   :lines: 20-21
   :dedent: 4
```

And declare our cats as candidates for it:

```eval_rst
.. literalinclude:: ../example/migrations/0003_elect_a_cat.py
   :language: python
   :lines: 23-27
   :dedent: 4
```
