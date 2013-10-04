# -*- encoding: utf-8 -*-

__version__ = "git"

try:
    from pkg_resources import get_distribution
    __version__ = get_distribution('pilot-client').version
except ImportError:
    pass

