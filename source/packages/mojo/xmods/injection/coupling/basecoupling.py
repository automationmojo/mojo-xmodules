"""
.. module:: basecoupling
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`BaseCoupling` class and associated reflection methods.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


import logging

from mojo.collections.contextuser import ContextUser

class BaseCoupling(ContextUser):
    """
        The :class:`BaseCoupling` object serves as a base type to detect coupling based
        resources.
    """

    logger = logging.getLogger()
