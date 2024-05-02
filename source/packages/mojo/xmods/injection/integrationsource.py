
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []


from typing import Callable

from mojo.xmods.injection.coupling.integrationcoupling import IntegrationCoupling

from mojo.xmods.injection.sourcebase import SourceBase

class IntegrationSource(SourceBase):

    def __init__(self, source_func: Callable, integration_type: IntegrationCoupling, constraints: dict):
        SourceBase.__init__(self, source_func, None, integration_type, constraints)
        return
