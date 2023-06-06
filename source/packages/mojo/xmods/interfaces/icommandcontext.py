"""
.. module:: icommandagent
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains a protocol for running commands, opening command
               sessions, and propagating an open session descendant apis.

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

from typing import Protocol, Optional, Sequence, Tuple, Union


from mojo.xmods.aspects import AspectsCmd


class ICommandContext(Protocol):
    """
        The :class:`ICommandContext` interface is used to provide a common interface for both SSH and Serial command runners.
    """

    def open_session(self, primitive: bool = False, cmd_context: Optional["ICommandContext"] = None,
                     aspects: Optional[AspectsCmd] = None) -> "ICommandContext": # pylint: disable=arguments-differ
        """
            Provides a mechanism to create a :class:`SshSession` object with derived settings.  This method allows various parameters for the session
            to be overridden.  This allows for the performing of a series of SSH operations under a particular set of shared settings and or credentials.

            :param primitive: Use primitive mode for FTP operations for the session.
            :param interactive: Creates an interactive session which holds open an interactive shell so commands can interact in the shell.
            :param cmd_context: An optional SshSession instance to use.  This allows re-use of sessions.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
