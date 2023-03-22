
from typing import Dict, Generator, List, Optional, Union

import logging
import threading

from mojo.xmods.xcollections.context import Context, ContextPaths

from mojo.xmods.exceptions import SemanticError

from mojo.xmods.landscaping.layers.landscapeconfigurationlayer import LandscapeConfigurationLayer
from mojo.xmods.landscaping.layers.landscapeinstallationlayer import LandscapeInstallationLayer
from mojo.xmods.landscaping.layers.landscapeintegrationlayer import LandscapeIntegrationLayer
from mojo.xmods.landscaping.layers.landscapeoperationallayer import LandscapeOperationalLayer
from mojo.xmods.landscaping.layers.topologyintegrationlayer import TopologyIntegrationLayer
from mojo.xmods.landscaping.landscapeparameters import (
    LandscapeActivationParams,
    DEFAULT_LANDSCAPE_ACTIVATION_PARAMS,
)
from mojo.xmods.landscaping.landscapedevice import LandscapeDevice
from mojo.xmods.landscaping.friendlyidentifier import FriendlyIdentifier

from mojo.xmods.landscaping.coupling.integrationcoupling import IntegrationCoupling

from mojo.xmods.xthreading.lockscopes import LockedScope, UnLockedScope
from mojo.xmods.xinspect import get_caller_function_name

class Landscape:
    """
        The base class for all derived :class:`Landscape` objects.  The :class:`Landscape`
        object is a singleton object that provides access to the resources and test
        environment level methods.  The functionality of the :class:`Landscape` object is setup
        so it can be transitioned through activation stages:
        
        * Configuration
        * Integration
        * Operational

        The different phases of operation of the landscape allow it to be used for a wider variety
        of purposes from commandline configuration and maintenance operations, peristent services
        and automation run functionality.

        The activation stages or levels of the :class:`Landscape` object are implemented using
        a python MixIn pattern in order to ensure that individual layers can be customized
        using object inheritance while at the same time keeping the object hierarchy simple.

        ..note: The :class:`Landscape` object constructor utilizes the `super` keyword for calling
                the mixin layer constructors using method resolution order or `mro`.  In order for
                `super` to work correctly all objects in the hierarchy should also provide a
                constructor and should also utilize `super`.  This is true also for objects that
                only inherit from :class:`object`. Should you need to create a custom layer override
                object, you must ensure the proper use of `super` in its constructor.
    """

    context = Context()
    logger = logging.getLogger()
    landscape_lock = threading.RLock()

    landscape_type = None
    interactive_mode: bool = False
    instance = None
    instance_initialized = False
    configuring_thread_id = None

    _configured_gate: threading.Event = threading.Event()
    _integration_gate: threading.Event = None
    _operational_gate: threading.Event = None

    def __new__(cls):
        """
            Constructs new instances of the Landscape object from the :class:`Landscape`
            type or from a derived type that is found in the module specified in the
            'MJR_CONFIG_EXTENSION_POINTS_MODULE' environment variable and overloading
            the 'get_landscape_type' method.
        """

        if Landscape.landscape_type is None:
            if Landscape.instance is None:
                Landscape.instance = super(Landscape, cls).__new__(cls)
        elif Landscape.instance is None:
            Landscape.instance = super(Landscape, cls.landscape_type).__new__(cls.landscape_type)

        return Landscape.instance

    def __init__(self):
        """
            Creates an instance or reference to the :class:`Landscape` singleton object.  On the first call to this
            constructor the :class:`Landscape` object is initialized and the landscape configuration is loaded.
        """

        # We are a singleton so we only want the intialization code to run once
        with self.begin_locked_landscape_scope() as lkscope:

            if not Landscape.instance_initialized:
                Landscape.instance_initialized = True
            
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    call_function_name = get_caller_function_name()
                    if call_function_name != "LandscapeSingleton":
                        errmsg = "The `Landscape` object should only be instantiated from `LandscapeSingleton`" \
                                "function located in the `mojoxmods.wellknown.singltons` module."
                        raise SemanticError(errmsg)

                    self._layer_install: LandscapeInstallationLayer = LandscapeInstallationLayer(self)
                    self._layer_configuration: LandscapeConfigurationLayer = LandscapeConfigurationLayer(self)
                    self._layer_integration: LandscapeIntegrationLayer = LandscapeIntegrationLayer(self)
                    self._layer_operational: LandscapeOperationalLayer = LandscapeOperationalLayer(self)
                    self._topology_description: TopologyIntegrationLayer = TopologyIntegrationLayer(self)
        
                    self._landscape_configure_complete = False
                    self._landscape_integrate_complete = False
                    self._landscape_startup_complete = False

                    self._devices_all: List[LandscapeDevice] = []

                    super().__init__()

        return
    
    @property
    def layer_configuration(self):
        """
            Gets the configuration layer for the current Landscape.
        """
        return self._layer_configuration

    @property
    def layer_install(self):
        """
            Gets the installation layer for the current Landscape.
        """
        return self._layer_install
    
    @property
    def layer_integration(self):
        """
            Gets the integration layer for the current Landscape.
        """
        return self._layer_integration
    
    @property
    def layer_operational(self):
        """
            Gets the operational layer for the current Landscape.
        """
        return self._layer_operational

    @property
    def installed_integration_couplings(self) -> Dict[str, IntegrationCoupling]:
        """
            Returns a table of the installed integration couplings found.
        """
        return self._layer_install.installed_integration_couplings

    def activate_configuration(self) -> None:
        """
            Called once at the beginning of the lifetime of a Landscape derived type in order
            to load the landscape, topology and runtime information.  
        """

        thisType = type(self)

        with self.begin_locked_landscape_scope() as lkscope:

            if thisType.configuring_thread_id is None:
                init_thread = threading.current_thread()
                thisType.configuring_thread_id = init_thread.ident

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    self._layer_configuration.load_landscape()

                    self._layer_configuration.load_topology()

                    log_configuration_declarations = thisType.context.lookup(ContextPaths.BEHAVIORS_LOG_CONFIGURATION, True)
                    if log_configuration_declarations:
                        log_to_directory = thisType.context.lookup(ContextPaths.OUTPUT_DIRECTORY)
                        self._layer_configuration.record_configuration(log_to_directory)

                    self._layer_configuration.initialize_credentials()

                    self._all_devices = self._layer_configuration.initialize_landscape()

                    self._landscape_configure_complete = True

                    # Set the landscape_initialized even to allow other threads to use the APIs of the Landscape object
                    self._configured_gate.set()
            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be initialized
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the contructor, wait
                    # for the first calling thread to finish initializing the
                    # Landscape before we return and try to use the returned
                    # Landscape reference
                    self._configured_gate.wait()

        return
    
    def activate_integration(self, *, activation_params: LandscapeActivationParams=DEFAULT_LANDSCAPE_ACTIVATION_PARAMS) -> None:
        """
            Called in order to mark the configuration process as complete in order
            for the activation stage to begin and to make the activation level methods
            callable.
        """
        thisType = type(self)

        with self.begin_locked_landscape_scope() as lkscope:

            if thisType._integration_gate is None:
                thisType._integration_gate = threading.Event()
                thisType._integration_gate.clear()

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    #TODO: Add integration code here

                    self._landscape_integrate_complete = True

                    self._integration_gate.set()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be activated
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the activate method,
                    # wait for the first calling thread to finish activating the
                    # Landscape before we return allowing other use of the Landscape
                    # singleton
                    self._integration_gate.wait()

        return

    def activate_operations(self, *, activation_params: LandscapeActivationParams=DEFAULT_LANDSCAPE_ACTIVATION_PARAMS) -> None:
        
        thisType = type(self)

        with self.begin_locked_landscape_scope() as lkscope:

            if thisType._operational_gate is None:
                thisType._operational_gate = threading.Event()
                thisType._operational_gate.clear()

                # We don't need to hold the landscape lock while initializing
                # the Landscape because no threads calling the constructor can
                # exit without the landscape initialization being finished.
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    self._activate_coordinators(activation_params)

                    self._establish_connectivity(activation_params)

                    self._validate_features(activation_params)

                    self._validate_topology(activation_params)

                    self._operational_gate.set()

            else:

                # Don't hold the landscape like while we wait for the
                # landscape to be activated
                with self.begin_unlocked_landscape_scope() as ulkscope:

                    # Because the landscape is a global singleton and because
                    # we were not the first thread to call the activate method,
                    # wait for the first calling thread to finish activating the
                    # Landscape before we return allowing other use of the Landscape
                    # singleton
                    self._operational_gate.wait()

        return

    def begin_locked_landscape_scope(self) -> "LockedScope":
        """
            Method that creates a locked scope for this device.
        """
        lkd_scope = LockedScope(self.landscape_lock)
        return lkd_scope

    def begin_unlocked_landscape_scope(self) -> "UnLockedScope":
        """
            Method that creates an unlocked scope for this device.
        """
        unlkd_scope = UnLockedScope(self.landscape_lock)
        return unlkd_scope
    
    def _create_layers(self):
        
        self._layer_install = LandscapeInstallationLayer(self)
        self._layer_configuration = LandscapeConfigurationLayer(self)
        self._layer_integration = LandscapeIntegrationLayer(self)
        self._layer_operational = LandscapeOperationalLayer(self)
        self._topology_description = TopologyIntegrationLayer(self)
        return

    def _activate_coordinators(self, activation_params: LandscapeActivationParams):

        return
    
    def _establish_connectivity(self, activation_params: LandscapeActivationParams):
        
        return
    
    def _validate_features(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_features:
            pass

        return
    
    def _validate_topology(self, activation_params: LandscapeActivationParams):

        if activation_params.validate_topology:
            pass

        return

def startup_landscape(activation_params: LandscapeActivationParams=DEFAULT_LANDSCAPE_ACTIVATION_PARAMS,
        interactive: Optional[bool]=None) -> Landscape:
    """
        Statup the landscape outside of a testrun.
    """

    from mojo.xmods.wellknown.singletons import LandscapeSingleton

    interactive_mode = False
    if interactive is not None:
        interactive_mode = interactive

    # ==================== Landscape Initialization =====================
    # The first stage of standing up the test landscape is to create and
    # initialize the Landscape object.  If more than one thread calls the
    # constructor of the Landscape, object, the other thread will block
    # until the first called has initialized the Landscape and released
    # the gate blocking other callers.

    # When the landscape object is first created, it spins up in configuration
    # mode, which allows consumers consume and query the landscape configuration
    # information.
    lscape = LandscapeSingleton()
    lscape.interactive_mode = interactive_mode

    lscape.activate_configuration()

    # After all the coordinators have had an opportunity to register with the
    # 'landscape' object, transition the landscape to the activated 'phase'
    lscape.activate_integration(activation_params=activation_params)

    # Finalize the activation process and transition the landscape
    # to fully active where all APIs are available.
    lscape.activate_operations(activation_params=activation_params)

    return lscape