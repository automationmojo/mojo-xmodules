__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


from typing import Any, Dict, List, Union

from mojo.xmods.injection.constraints import Constraints, FeatureConstraints, ConstraintsRef, ConstraintSource


class ConstraintsCatalog:
    """
        The :class:`ConstraintCatalog` object is a singleton that stores the constraints for an automation run
        and provides a way to pass constraints from multiple sources to tests.
    """

    _instance = None
    _initialized = False


    def __new__(cls):
        """
            Constructs new instances of the ResourceRegistry object.
        """
        if cls._instance is None:
            cls._instance = super(ConstraintsCatalog, cls).__new__(cls)

        return cls._instance


    def __init__(self):
        """
            Initializes the SubscriptionRegistry object the first time this singleton is created.
        """
        thisType = type(self)

        if not thisType._initialized:
            thisType._initialized = True

            self._site_constraints: Dict[str, ConstraintsRef] = {}
            self._override_constraints: Dict[str, ConstraintsRef] = {}

        return


    def add_constraints(self, constraints_ref: ConstraintsRef):

        source = constraints_ref.source
        scope = constraints_ref.scope

        if source == ConstraintSource.SITE_PARAMETER:
            self._site_constraints[scope] = constraints_ref
        elif source == ConstraintSource.OVERRIDE_PARAMETER:
            self._override_constraints[scope] = constraints_ref
        else:
            raise ValueError(f"Unkown constraint source='{source}' scope='{scope}'")
        
        return
    

    def lookup_constraints(self, scope: str) -> Union[Constraints, FeatureConstraints, Dict[str, Any]]:
        """
            Looks up a constraint by its 'scope' name based on order of priority.  Override constraints take
            priority over factory site constraints.
        """
        rtnval = None

        if scope in self._override_constraints:
            cref = self._override_constraints[scope]
            rtnval = cref.constraints
        elif scope in self._site_constraints:
            cref = self._site_constraints[scope]
            rtnval = cref.constraints
        
        return rtnval


    def prune_constraints(self, keep_scopes: List[str]):
        """
            Prunes the constraints catalog down to a specified list of scopes that are relevant to the current
            injection environment.
        """
        
        pruned_constraints = {}
        for scope in keep_scopes:
            if scope in self._site_constraints:
                pruned_constraints[scope] = self._site_constraints[scope]

        self._site_constraints = pruned_constraints

        pruned_constraints = {}
        for scope in keep_scopes:
            if scope in self._override_constraints:
                pruned_constraints[scope] = self._override_constraints[scope]

        self._override_constraints = pruned_constraints

        return