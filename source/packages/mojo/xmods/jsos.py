"""
.. module:: jsos
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains constants and functions for working with jsos file format.

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

from typing import Any, Dict, List

import json

CHAR_RECORD_SEPERATOR = "\x1E\n"

def load_jsos_stream_from_file(filename: str) -> List[Dict[str, Any]]:

    json_items = []

    with open(filename, 'r') as sf:
        stream_content = sf.read()
        stream_content = stream_content.strip(CHAR_RECORD_SEPERATOR)
    
        str_items = stream_content.split(CHAR_RECORD_SEPERATOR)
        for sitem in str_items:
            jitem = json.loads(sitem)
            json_items.append(jitem)

    return json_items
