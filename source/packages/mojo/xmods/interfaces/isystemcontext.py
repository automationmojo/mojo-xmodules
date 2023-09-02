"""
.. module:: isystemagent
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains a protocol for running system commands and working with
               system files.  

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


class ISystemContext(Protocol):
    """
        The :class:`ISystemContext` interface is used to provide a common interface for both SSH and Serial command runners.
    """

    def directory(self, rootdir: str) -> dict:
        """
            Method that creates a directory listing for the folder.

            :param rootdir: The directory to scan when creating the tree.

            :returns: A dictionary that contains information about the items in the target directory.
        """

    def directory_exists(self, tgtdir: str) -> bool:
        """
            Method used to pull a remote directory to check for existance.

            :param remotedir: The remote directory path to check for existance.

            :returns: A boolean value indicating if the remote file exists.
        """
    
    def directory_tree(self, rootdir: str, depth: int = 1) -> dict:
        """
            Method that creates a directory tree for the folder.

            :param root_dir: The root directory to scan when creating the tree.
            :param depth: The dept to scan to

            :returns: A dictionary with a tree of information about the directory tree found on the remote system.
        """
    
    def file_exists(self, filepath: str) -> bool:
        """
            Method used to pull a remote file to check for existance.

            :param remotepath: The remote file path to check for existance.

            :returns: A boolean value indicating if the remote file exists.
        """

    def file_pull(self, remotepath: str, localpath: str):
        """
            Method used to pull a remote file to a local file path.

            :param remotepath: The remote file path to pull to the local file.
            :param localpath: The local file path to pull the content to.
        """

    def file_push(self, localpath: str, remotepath: str):
        """
            Method used to push a local file to a remote file path.

            :param localpath: The local file path to push the content of to the remote file.
            :param remotepath: The remote file path to push content to.
        """

    def open_session(self, sysctx: Optional["ISystemContext"] = None, aspects: Optional[AspectsCmd] = None) -> "ISystemContext": # pylint: disable=arguments-differ
        """
            Provides a mechanism to create a :class:`SshSession` object with derived settings.  This method allows various parameters for the session
            to be overridden.  This allows for the performing of a series of SSH operations under a particular set of shared settings and or credentials.

            :param primitive: Use primitive mode for FTP operations for the session.
            :param interactive: Creates an interactive session which holds open an interactive shell so commands can interact in the shell.
            :param sysctx: An optional ISystemContext instance to use for creating a session.  This allows arbitrary re-use of sessions.
            :param aspects: The default run aspects to use for the operations performed by the session.
        """

    def reboot(self, aspects: Optional[AspectsCmd] = None):
        """
            Reboots the designated host by running the 'reboot' command on the host.
            
            ..note: This method is not a typical SSH functionality, but it was added so that
                    automatic reconnects can be implemented as required on session objects.

        """

    def run_cmd(self, command: str, exp_status: Union[int, Sequence]=0, aspects: Optional[AspectsCmd] = None) -> Tuple[int, str, str]: # pylint: disable=arguments-differ
        """
            Runs a command on the designated host using the specified parameters.

            :param command: The command to run.
            :param exp_status: An integer or sequence of integers that specify the set of expected status codes from the command.
            :param aspects: The run aspects to use when running the command.

            :returns: The status, stderr and stdout from the command that was run.
        """
    
    def verify_connectivity(self) -> bool:
        """
            Method that can be used to verify connectivity to the target computer.

            :returns: A boolean value indicating whether connectivity with the remote machine was successful.
        """
