
from typing import Any, Optional

import sys

import click

def get_argv_encoding() -> str:
    return getattr(sys.stdin, "encoding", None) or sys.getfilesystemencoding()

class NormalizedStringParamType(click.ParamType):
    name = "text"

    def convert(self, value: Any, param: Optional["click.Parameter"], ctx: Optional["click.Context"]) -> Any:
        
        if isinstance(value, bytes):
            enc = get_argv_encoding()
            try:
                value = value.decode(enc)
            except UnicodeError:
                fs_enc = sys.getfilesystemencoding()
                if fs_enc != enc:
                    try:
                        value = value.decode(fs_enc)
                    except UnicodeError:
                        value = value.decode("utf-8", "replace")
                else:
                    value = value.decode("utf-8", "replace")
        else:
            value = str(value)

        if len(value) > 1:
            # If our string is quoted, normalize the string by remove the quotes.
            first_char = value[0]
            last_char = value[-1]
            if (first_char == "'" and last_char == "'") or \
            (first_char == '"' and last_char == '"'):
                value = value[1:-1]

        return value


    def __repr__(self) -> str:
        return "NORMALIZED_STRING"

NORMALIZED_STRING = NormalizedStringParamType()
