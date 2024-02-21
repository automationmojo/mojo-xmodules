__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"


from typing import Any, Dict, List, Union

from mojo.xmods.injection.constraints import Constraints, FeatureConstraints, ConstraintsRef, ConstraintsOrigin

def create_constraint_key(source: str, identifier: str):
    return f"{source}:{identifier}"

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


    def add_constraints(self, origin: ConstraintsOrigin, originating_scope: str, identifier: str, constraints: Union[Constraints, FeatureConstraints, Dict[str, Any]]) -> str:

        ckey = create_constraint_key(originating_scope, identifier)

        cref = ConstraintsRef(origin, originating_scope, identifier, constraints)

        if origin == ConstraintsOrigin.SITE_PARAMETER:
            self._site_constraints[ckey] = cref
        elif origin == ConstraintsOrigin.OVERRIDE_PARAMETER:
            self._override_constraints[ckey] = cref
        else:
            raise ValueError(f"Unkown constraint origin='{origin}' scope='{originating_scope}' identifier={identifier}")
        
        return ckey
    

    def lookup_constraints(self, constraints_key: str) -> Union[Constraints, FeatureConstraints, Dict[str, Any]]:
        """
            Looks up a constraint by its 'scope' name based on order of priority.  Override constraints take
            priority over factory site constraints.
        """

        rtnval = None

        if constraints_key in self._override_constraints:
            cref = self._override_constraints[constraints_key]
            rtnval = cref.constraints
        elif constraints_key in self._site_constraints:
            cref = self._site_constraints[constraints_key]
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