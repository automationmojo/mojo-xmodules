
import unittest

import time

from mojo.xmods.xdatetime import (
    current_time_millis,
    format_time_with_fractional,
    parse_datetime
)

class TestEnhancer(unittest.TestCase):
    
    def test_current_time_millis(self):
        before = time.time() * 1000
        ctm = current_time_millis()
        assert ctm - before > 0, f"Current time should be after. before={before} ctm={ctm}"
        
        diff = ctm - before
        assert diff < .01, f"The time diff should be less then .01. before={before} ctm={ctm} diff={diff}"
    
    def test_format_and_parse_timestamp(self):
        now = time.time()
        before = round(now, 6)
        ftime = format_time_with_fractional(now)
        ptime = parse_datetime(ftime)
        after = ptime.timestamp()
        assert before == after, f"The after time should have equaled before time.  before={before} ftime={ftime} ptime={ptime} after={after}"


if __name__ == '__main__':
    unittest.main()
