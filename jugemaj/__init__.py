"""Main module entrance."""

try:
    from importlib.metadata import version
    __version__ = version('django_jugemaj')
    __version_info__ = tuple(int(i) for i in __version__.split('.'))
except ModuleNotFoundError:  # Python < 3.7
    pass
