"""
.. module:: xformatting
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains functions for formatting text.

.. note:: The modules that are named `xsomething` like this module are prefixed with an `x` character to
          indicate they extend the functionality of a base python module and the `x` is pre-pended to
          prevent module name collisions with python modules.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []



from typing import List, Optional, Union

import os

from io import StringIO

class CommandOutputFormat:
    DISPLAY = 0
    JSON = 1
    YAML = 2

def format_command_result(msg: str, command: str, status: int, stdout: str, stderr: str, exp_status: Optional[List[int]]=None, target: Optional[str]=None) -> str:
    """
        Takes a message and command results and formats a message for output to the logs.

        :param msg: The message to output to the logs
        :param command: The command that was run.
        :param status: The return status code associated with the command.
        :param stdout: The std out text from the command.
        :param stderr: The std error text from the command.
        :param exp_status: The expected status from the command.
        :param target: The target the command was run against.

        :returns: The formatted message output.
    """

    fmt_msg_lines = [msg]

    if target is not None:
        fmt_msg_lines.append("TARGET: {}".format(target))

    fmt_msg_lines.append("COMMAND {}".format(command))
    fmt_msg_lines.append("STATUS: {}".format(status))

    if exp_status is not None:
        fmt_msg_lines.append("EXPECTED: {}".format(repr(exp_status)))

    if stdout is not None and len(stdout.strip()) > 0:
        fmt_msg_lines.append("STDOUT:")
        fmt_msg_lines.append(indent_lines(stdout, 1))

    if stderr is not None and len(stderr.strip()) > 0:
        fmt_msg_lines.append("STDERR:")
        fmt_msg_lines.append(indent_lines(stderr, 1))

    fmt_msg = os.linesep.join(fmt_msg_lines)

    return fmt_msg

def indent_lines(msg: str, level: int, indent: int=4) -> str:
    """
        Takes a string and splits it into multiple lines, then indents each line
        to the specified level using 'indent' spaces for each level.

        :param msg: The text content to split into lines and then indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.

        :returns: The indenting content
    """
    # Split msg into lines keeping the line endings
    msglines = msg.splitlines(True)

    pfx = " " * (level * indent)

    indented = StringIO()
    for nxtline in msglines:
        indented.write(pfx)
        indented.write(nxtline)

    return indented.getvalue()

def indent_line(lcontent: str, level: int, indent: int, pre_strip_leading: bool=True) -> str:
    """
        Takes a string and indents it to the specified level using 'indent' spaces
        for each level.

        :param lcontent: The text line to indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.
        :param pre_strip_leading: Strip any leading whitesspace before indenting the line.

        :returns: The indented line
    """
    pfx = " " * (level * indent)

    indented = None
    if pre_strip_leading:
        indented = "{}{}".format(pfx, lcontent.lstrip())
    else:
        indented = "{}{}".format(pfx, lcontent)

    return indented

def indent_lines_list(msglines: List[str], level: int, indent: int=4) -> List[str]:
    """
        Takes a list of str that has already been split on new-lines and indents each line
        to the specified level using 'indent' spaces for each level.

        :param msglines: The list of text lines to indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.

        :returns: The indenting lines
    """
    outlines = [] 

    pfx = " " * (level * indent)

    for nxtline in msglines:
        outlines.append(f"{pfx}{nxtline}")

    return outlines

def split_and_indent_lines(msg: str, level: int, indent: int=4, pre_strip_leading: bool=True) -> List[str]:
    """
        Takes a string and splits it into multiple lines, then indents each line
        to the specified level using 'indent' spaces for each level.

        :param msg: The text content to split into lines and then indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.
        :param pre_strip_leading: Strip any leading whitesspace before indenting the lines.

        :returns: The indenting lines
    """

    # Split msg into lines keeping the line endings
    msglines = msg.splitlines(False)

    prestrip_len = len(msg)
    if pre_strip_leading:
        for nxtline in msglines:
            stripped = nxtline.lstrip()
            striplen = len(nxtline) - len(stripped)
            if striplen < prestrip_len:
                prestrip_len = striplen

    pfx = " " * (level * indent)

    indented = None
    if pre_strip_leading and prestrip_len > 0:
        indented = [pfx + nxtline[prestrip_len:] for nxtline in msglines]
    else:
        indented = [pfx + nxtline for nxtline in msglines]

    return indented
