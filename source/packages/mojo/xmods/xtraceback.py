__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import traceback

def format_exc_lines():
    """
        Gets a 'format_exc' result and splits it into mutliple lines.
    """
    rtn_lines = traceback.format_exc().splitlines()
    return rtn_lines