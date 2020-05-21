"""Main module entrance."""

try:
    # Waiting for something better in https://github.com/python-poetry/poetry/issues/144
    from importlib.metadata import version
    __version__ = version('django_jugemaj')
    __version_info__ = tuple(int(i) for i in __version__.split('.'))
except ModuleNotFoundError:  # Python < 3.7
    pass
