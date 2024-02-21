__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import Any, Dict, List, Union

from enum import Enum

from mojo.xmods.xfeature import FeatureMask, FeatureTag


class ConstraintSource(str, Enum):
    SITE_PARAMETER = "site-parameter"
    OVERRIDE_PARAMETER = "override-parameter"


class Constraints(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return

    def __call__(self, **kwargs: Any):
        inst = dict(self)
        inst.update(kwargs)
        return inst


class FeatureConstraintKeys(str, Enum):
    REQUIRED_FEATURES = "required_features"
    EXCLUDED_FEATURES = "excluded_features"


class FeatureConstraints(FeatureMask):

    def __init__(self, *, required_features: List[FeatureTag]=None,
                       excluded_features: List[FeatureTag]=None,
                       checkout: bool=False, **kwargs):
        super().__init__(required_features=required_features,
                         excluded_features=excluded_features,
                         checkout=checkout, **kwargs)
        return

    def __call__(self, **kwargs: Any):
        inst = dict(self)
        inst.update(kwargs)
        return inst


class ConstraintsRef:

    def __init__(self, source: ConstraintSource, scope: str, constraints: Constraints):
        self._source = source
        self._scope = scope
        self._constraints = constraints
        return

    @property
    def constraints(self) ->  Union[Constraints, FeatureConstraints, Dict[str, Any]]:
        return self._constraints
    
    @property
    def scope(self):
        return self._scope
    
    @property
    def source(self):
        return self._source


def merge_constraints(*args: Union[Constraints, dict]) -> Constraints:
    """
        Takes a sequence of :class:`Contraints` objects and merges them into a single
        :class:`Constraints` object.

        ..note: In cases where this method is provided with constraints with overlapping
                values, the last constraint with a give value will overwrite any previous
                values.
    """

    combined: Constraints = Constraints()

    for av in args:
        combined.update(av)
    
    return combined

