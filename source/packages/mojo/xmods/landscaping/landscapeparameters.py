"""
.. module:: landscapeparameters
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeActivationParams` class which provides an
               overloadable and function signature friendly way to provide customizable parameters
               to the landscape startup functions.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

from types import SimpleNamespace

class LandscapeActivationParams(SimpleNamespace):
    allow_missing_devices: bool=False
    allow_unknown_devices: bool=False
    validate_features: bool=True
    validate_topology: bool=True

DEFAULT_LANDSCAPE_ACTIVATION_PARAMS = LandscapeActivationParams()
