
from typing import Dict, List, Optional

import io
import logging
import shutil
import tempfile
import unittest

from uuid import uuid4

from mojo.collections.context import Context
from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton

from mojo.xmods.autoclean import create_autoclean_tempdir_scope
from mojo.xmods.xlogging.foundations import (
    logging_initialize,
    SWAPPABLE_HOOKS
)
from mojo.xmods.xlogging.levels import LogLevel

MSG_UUID = str(uuid4())
TEST_LOG_MESSAGE = f"This is a sample log message '{MSG_UUID}'"

class LogLevelTests(unittest.TestCase):

    def setUp(self):
        self._context: Context = ContextSingleton()
        self._context.insert(ContextPaths.JOB_TYPE, "testrun")
        
        self._artifacts_dir = tempfile.mkdtemp(prefix="mojo_xmods_tests")

        return

    def tearDown(self) -> None:
        shutil.rmtree(self._artifacts_dir, ignore_errors=True)
        return

    def test_log_critical_excluded(self):

        consolelevel = LogLevel.QUIET
        logfilelevel = LogLevel.QUIET
        logname_template = f"test_log_critical_excluded.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.critical(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 0, "The log message SHOULD NOT be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return
    
    def test_log_critical_included(self):

        consolelevel = LogLevel.CRITICAL
        logfilelevel = LogLevel.CRITICAL
        logname_template = f"test_log_critical_included.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.critical(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 1, "The log message SHOULD be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 1, "The 'stderr' file SHOULD NOT have the output."

        return

    def test_log_debug_excluded(self):

        consolelevel = LogLevel.INFO
        logfilelevel = LogLevel.INFO
        logname_template = f"test_log_debug_excluded.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.debug(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 0, "The log message SHOULD NOT be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return
    
    def test_log_debug_included(self):

        consolelevel = LogLevel.DEBUG
        logfilelevel = LogLevel.DEBUG
        logname_template = f"test_log_debug_included.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.debug(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 1, "The log message SHOULD be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 1, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return

    def test_log_error_excluded(self):

        consolelevel = LogLevel.CRITICAL
        logfilelevel = LogLevel.CRITICAL
        logname_template = f"test_log_error_excluded.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.error(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 0, "The log message SHOULD NOT be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return
    
    def test_log_error_included(self):

        consolelevel = LogLevel.ERROR
        logfilelevel = LogLevel.ERROR
        logname_template = f"test_log_error_included.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.error(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 1, "The log message SHOULD be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 1, "The 'stderr' file SHOULD NOT have the output."

        return

    def test_log_info_excluded(self):

        consolelevel = LogLevel.WARNING
        logfilelevel = LogLevel.WARNING
        logname_template = f"test_log_info_excluded.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.info(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 0, "The log message SHOULD NOT be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return
    
    def test_log_info_included(self):

        consolelevel = LogLevel.INFO
        logfilelevel = LogLevel.INFO
        logname_template = f"test_log_info_included.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.info(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 1, "The log message SHOULD be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 1, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return

    def test_log_warning_excluded(self):

        consolelevel = LogLevel.ERROR
        logfilelevel = LogLevel.ERROR
        logname_template = f"test_log_warning_excluded.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.warn(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 0, "The log message SHOULD NOT be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stderr' file SHOULD NOT have the output."

        return
    
    def test_log_warning_included(self):

        consolelevel = LogLevel.WARNING
        logfilelevel = LogLevel.WARNING
        logname_template = f"test_log_warning_included.log"

        test_temp_dir = tempfile.mkdtemp(dir=self._artifacts_dir)
        logfile, stdout, stderr = self._reinitialize_logging(test_temp_dir, consolelevel, logfilelevel, logname_template)

        logging.warn(TEST_LOG_MESSAGE)

        found = self._contains_log_entry(logfile, TEST_LOG_MESSAGE)
        assert found == 1, "The log message SHOULD be found."

        found = self._contains_output_entry(stdout, TEST_LOG_MESSAGE)
        assert found == 0, "The 'stdout' file SHOULD NOT have the output."

        found = self._contains_output_entry(stderr, TEST_LOG_MESSAGE)
        assert found == 1, "The 'stderr' file SHOULD NOT have the output."

        return
        
    def _contains_log_entry(self, logfile: str, entry: str) -> int:

        content_lines = None
        with open(logfile, 'r') as lf:
            content_lines = lf.readlines()

        found = 0
        for line in content_lines:
            line = line.strip()
            if line.find(TEST_LOG_MESSAGE) > -1:
                found = found + 1

        return found

    def _contains_output_entry(self, stream: io.StringIO, entry: str) -> int:

        found = 0

        content_lines = stream.getvalue().splitlines(False)
        for line in content_lines:
            if line.find(entry) > -1:
                found = found + 1

        return found

    def _insert_logging_branch(self, branch_configs: List[Dict[str, str]], logger_name: str, log_file_name: str, log_level: str):

        new_branch = {
            "name": logger_name,
            "logname": log_file_name,
            "loglevel": log_level
        }

        branch_configs.append(new_branch)

        return

    def _reinitialize_logging(self, output_directory: str, consolelevel: int, logfilelevel: int,
                              logname_template: str, logging_branches: Optional[Dict[str, str]]=None) -> str:

        mem_stdout = io.StringIO()
        SWAPPABLE_HOOKS.HOOK_SYS_STDOUT = mem_stdout

        mem_stderr = io.StringIO()
        SWAPPABLE_HOOKS.HOOK_SYS_STDERR = mem_stderr

        # Set the appropriate logging information in the context and then
        # call 'logging_initialize' to trigger the re-initialization of logging

        self._context.insert(ContextPaths.OUTPUT_DIRECTORY, output_directory)
        self._context.insert(ContextPaths.LOGGING_LEVEL_CONSOLE, consolelevel)
        logfilelevel =  self._context.insert(ContextPaths.LOGGING_LEVEL_LOGFILE, logfilelevel)
        logname_template =  self._context.insert(ContextPaths.LOGGING_LOGNAME, logname_template)

        if logging_branches is not None:
            self._context.insert(ContextPaths.LOGGING_BRANCHED, logging_branches)
        else:
            self._context.insert(ContextPaths.LOGGING_BRANCHED, [])

        logfile = logging_initialize(reinitialize=True)

        return logfile, mem_stdout, mem_stderr

    
if __name__ == '__main__':
    unittest.main()
