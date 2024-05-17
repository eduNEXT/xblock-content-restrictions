"""
Modulestore generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def modulestore(*args, **kwargs):
    """
    Wrapper for `xmodule.modulestore.django.modulestore`
    """
    backend_function = settings.CONTENT_RESTRICTIONS_MODULESTORE_BACKEND
    backend = import_module(backend_function)

    return backend.modulestore(*args, **kwargs)
