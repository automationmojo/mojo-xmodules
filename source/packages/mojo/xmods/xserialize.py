"""
.. module:: xserialize
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains functions for serializing objects that implement the ISerializable protocol

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import List, Optional

import io
import yaml

from mojo.errors.exceptions import SemanticError

from mojo.interfaces.iserializable import ISerializable


def serializable_object_to_yaml(obj: ISerializable, line_indent: Optional[str] = None) -> List[str]:
    """
        Converts an object that implements ISerializable to a yaml representation.

        :param obj: The object to convert to yaml

        ..note: This method is especially useful for formatting complex output for display in a log
                since JSON and other formats are not as log friendly.
    """

    if not hasattr("as_dict", obj):
        errmsg = "Objects must implement the 'ISerializable' interface."
        raise SemanticError(errmsg)

    obj_as_dict = obj.as_dict()

    str_stream = io.StringIO()
    yaml.dump(obj_as_dict, str_stream, indent=4, default_flow_style=False)

    content = str_stream.getvalue()

    content_lines = content.splitlines(False)
    if line_indent is not None:
        content_lines = [f"{line_indent}{nxtline}" for nxtline in content_lines]

    return content_lines