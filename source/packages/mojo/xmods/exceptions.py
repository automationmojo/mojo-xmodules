"""
.. module:: exceptions
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains exceptions not provided by the standard python libraries.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

class AbstractMethodError(RuntimeError):
    """
        This error is raised when an abstract method has been called.
    """


class CommandError(RuntimeError):
    """
        This error is the base error for command results errors.
    """
    def __init__(self, message, status, stdout, stderr, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        return


class CheckinError(RuntimeError):
    """
        This error is raised when an error occurs during the checking in of a resource.
    """

class CheckoutError(RuntimeError):
    """
        This error is raised when an error occurs during the checkout of a resource.
    """

class ConfigurationError(BaseException):
    """
        The base error object for errors that indicate that there is an issue related
        to improper configuration.
    """

class InvalidConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object has been passed invalid configuration parameters.
    """

class LooperError(RuntimeError):
    """
        This error is raised when an error occurs with the use of the :class:`LooperPool` or
        :class:`Looper` objects.
    """

class LooperQueueShutdownError(LooperError):
    """
        This error is raised when work is being queued on a :class:`LooperQueue` thaat has
        been shutdown and when a worker thread is attempting to wait for work on an empty
        queue.
    """

class MissingConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object is missing required configuration parameters.
    """


class NotOverloadedError(RuntimeError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """

class NotSupportedError(RuntimeError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """

class SemanticError(BaseException):
    """
        The base error object for errors that indicate that there is an issue with
        a piece of automation code and with the way the Automation Kit code is being
        utilized.
    """
