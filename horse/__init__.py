import pkg_resources

from .app import build_app

__version__ = pkg_resources.require("horse")[0].version
__author__ = 'Pragmatic Coders <contact@pragmaticcoders.com>'
__all__ = ['build_app']
