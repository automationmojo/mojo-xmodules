
from types import SimpleNamespace

class LandscapeOperationsParams(SimpleNamespace):
    allow_missing_devices: bool=False
    allow_unknown_devices: bool=False
    validate_features: bool=True
    validate_topology: bool=True

DEFAULT_LANDSCAPE_OPERATIONS_PARAMS = LandscapeOperationsParams()