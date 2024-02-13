"""
.. module:: foundations
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains framework logging functions which extend the functionality to
        the python :module:`logging` module.
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

from typing import Optional, Union

import logging
import os
import sys
import tempfile
import traceback


from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton


from mojo.xmods.fspath import get_expanded_path
from mojo.xmods.xlogging.levels import LogLevel


DEFAULT_LOGGER_NAME = "AKIT"

LOGGING_SECTION_MARKER = "="
LOGGING_SECTION_MARKER_LENGTH = 80

DEFAULT_LOGFILE_FORMAT = '[%(asctime)s][%(name)s][%(levelname)s][%(message)s]'


class SWAPPABLE_HOOKS:
    # We capture references to sys.stdout and sys.stderr here so we can
    # swap out the file descriptor used by logging for testing purposes
    HOOK_SYS_STDOUT = sys.stdout
    HOOK_SYS_STDERR = sys.stderr


def format_log_section_header(title):
    """
        Formats a log section header by centering the title inside of the section marker character string.
    """
    title_upper = " %s " % title.strip().upper()
    marker_count = LOGGING_SECTION_MARKER_LENGTH - len(title_upper)
    marker_half = marker_count >> 1
    marker_prefix = LOGGING_SECTION_MARKER * marker_half
    marker_suffix = LOGGING_SECTION_MARKER * (marker_count - marker_half)
    header = "\n%s%s%s\n" % (marker_prefix, title_upper, marker_suffix)
    return header



class LoggingDefaults:
    """
        Makes all the default values associated with logging available.
    """
    DefaultFileLoggingHandler = logging.FileHandler



class EnhancedLogger(logging.Logger):

    def render(self, line):
        """
            Logs a message to both the standard in and to the log file.
        """
        self.info(line)
        print(line, file=SWAPPABLE_HOOKS.HOOK_SYS_STDOUT)
        return

    def section(self, title):
        """
            Logs a log section marker
        """
        marker = format_log_section_header(title)

        self.log(LogLevel.NOTSET, marker)
        print(marker, file=SWAPPABLE_HOOKS.HOOK_SYS_STDOUT)
        return

    def test_begin(self, testname, **test_args):
        """
        """
        info_msg_lines = [
            "TEST BEGIN - {}".format(testname),
            "    ARGS:"
        ]

        for arg_name, arg_value in test_args.items():

            arg_value_debug = None
            if hasattr(arg_value, "__debug_repr__"):
                arg_value_debug= arg_value.__debug_repr__()
            else:
                arg_value_debug = str(arg_value)

            info_msg_lines.append("    {} = {}".format(arg_name, arg_value_debug))

        info_msg = os.linesep.join(info_msg_lines)

        self.info(info_msg)
        print(info_msg, file=SWAPPABLE_HOOKS.HOOK_SYS_STDOUT)
        return

    def test_end(self, testname):
        info_msg = "TEST END - {}".format(testname)
        
        self.info(info_msg)
        print(info_msg, file=SWAPPABLE_HOOKS.HOOK_SYS_STDOUT)
        return


logging.setLoggerClass(EnhancedLogger)


class EnhancedRootLogger(EnhancedLogger):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """
    def __init__(self, level):
        """
        Initialize the logger with the name "root".
        """
        EnhancedLogger.__init__(self, "root", level)

    def __reduce__(self):
        return logging.getLogger, ()
    
    def adopt_children(self, other_root: logging.RootLogger):

        # Tell all of the root loggers children that we are the new parent
        children_of_root = [c for c in other_root.manager.loggerDict.values()]
        for child in children_of_root:
            if hasattr(child, "parent") and child.parent is other_root:
                child.parent = self

        return


class LessThanRecordFilter(logging.Filter):
    """
        Filters records with a log level < WARNING
    """

    def __init__(self, filter_at_level):
        super(LessThanRecordFilter, self).__init__("LessThanFilter")

        if isinstance(filter_at_level, str):
            filter_at_level = logging.getLevelName(filter_at_level)

        self._filter_at_level = filter_at_level
        return

    def filter(self, record): # pylint: disable=no-self-use
        """
            Performs the filtering of records.
        """
        process_rec = record.levelno < self._filter_at_level
        return process_rec
    

class GreaterOrEqualRecordFilter(logging.Filter):
    """
        Filters records with a log level < WARNING
    """

    def __init__(self, filter_at_level):
        super(GreaterOrEqualRecordFilter, self).__init__("GreaterOrEqualFilter")

        if isinstance(filter_at_level, str):
            filter_at_level = logging.getLevelName(filter_at_level)

        self._filter_at_level = filter_at_level
        return

    def filter(self, record): # pylint: disable=no-self-use
        """
            Performs the filtering of records.
        """
        process_rec = record.levelno >= self._filter_at_level
        return process_rec
    


logging_initialized = False

last_logfile = None


def logging_initialize(reinitialize: bool=False) -> str:
    """
        Method used to configure the automation kit logging based on the environmental parameters
        specified and then reinitialize the logging.

        ..note: Make sure the context path 'ContextPaths.OUTPUT_DIRECTORY' variable is set before
                calling 'logging_initialize'
    """
    logfile = None

    global logging_initialized
    global last_logfile

    if reinitialize or not logging_initialized:

        logging_initialized = True

        ctx = ContextSingleton()

        consolelevel = ctx.lookup(ContextPaths.LOGGING_LEVEL_CONSOLE, "INFO")
        logfilelevel = ctx.lookup(ContextPaths.LOGGING_LEVEL_LOGFILE, "DEBUG")
        logname_template = ctx.lookup(ContextPaths.LOGGING_LOGNAME, "{jobtype}.log")
        jobtype = ctx.lookup(ContextPaths.JOB_TYPE, "application")
        
        logname = logname_template.format(jobtype=jobtype)

        output_directory = get_expanded_path(ctx.lookup(ContextPaths.OUTPUT_DIRECTORY))
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        log_branches = ctx.lookup(ContextPaths.LOGGING_BRANCHED, [])

        # Setup the log files
        logfile = _reinitialize_logging(consolelevel, logfilelevel, output_directory, logname, log_branches)
        last_logfile = logfile
    else:
        logfile = last_logfile

    return logfile


def logging_create_branch_logger(logger_name: str, logfilename: str, log_level: Optional[Union[int, str]]=None):
    """
        Method that allows for the creation of a separate logfile for specific loggers in order
        to reduce the noise in the main logfile.  A common use for this would be to redirect
        logging from specific modules such as 'paramiko' and 'httplib' to thier own log files.
        :param logger_name: The name of the logger to create a branch log for.
    """
    root_logger = logging.getLogger()

    if logger_name in root_logger.manager.loggerDict:
        target_logger = logging.getLogger(logger_name)

        # Setup the relevant log file which will get all the
        # log entries from loggers that satisified a relevant
        # logger name prefix match
        handler = logging.FileHandler(logfilename)
        handler.setLevel(log_level)
        for handler in target_logger.handlers:
            target_logger.removeHandler(handler)
        target_logger.addHandler(handler)

    print("blah")

    return


def _reinitialize_logging(consolelevel, logfilelevel, output_dir, logfile_basename, log_branches) -> str:
    """
        Helper method to re-initialize the logging when the path to the output directory changes
        shortly after startup of the framework.  This method also handles the configuration of
        output levels, stdout and stderr file wrappers.
    """

    basecomp, extcomp = os.path.splitext(logfile_basename)

    ctx = ContextSingleton()

    debug_logfilename = os.path.join(output_dir, basecomp + ".DEBUG" + extcomp)
    
    ctx.insert(ContextPaths.LOGFILE_DEBUG, debug_logfilename)
    
    rel_logfilename = os.path.join(output_dir, basecomp + extcomp)


    # Swap out the root logger
    other_root_logger = logging.Logger.root

    root_logger = EnhancedRootLogger(logging.NOTSET)
    root_logger.adopt_children(other_root_logger)

    logging.root = root_logger
    logging.Logger.root = root_logger
    logging.Logger.manager.root = root_logger
    
    # Remove all the root handlers, this should not effect the logger
    # hierarchy
    root_handlers = [h for h in root_logger.handlers]

    for handler in root_handlers:
        root_logger.removeHandler(handler)

    # Any logging level that is set on the root logger would end up being
    # an effective level for any of the child loggers.  Set the root logger
    # to NOTSET, so we don't impose an effective log level on child loggers
    root_logger.setLevel(logging.NOTSET)


    # Setup the debug logfile, have everything go to the debug log file
    base_handler = LoggingDefaults.DefaultFileLoggingHandler(debug_logfilename)
    base_handler.setFormatter(logging.Formatter(DEFAULT_LOGFILE_FORMAT))
    base_handler.setLevel(logging.NOTSET)
    root_logger.addHandler(base_handler)


    # Setup the relevant log file which will get all the log entries from
    # loggers meet the log level constraints and that have not been handled
    # by other loggers.
    rel_handler = LoggingDefaults.DefaultFileLoggingHandler(rel_logfilename)
    rel_handler.setFormatter(logging.Formatter(DEFAULT_LOGFILE_FORMAT))
    rel_handler.setLevel(logfilelevel)
    root_logger.addHandler(rel_handler)


    # Setup the stdout logger with the correct console level and
    # filter the log entries from the stdout handler that are
    # greater than Info level

    stdout_handler = logging.StreamHandler(SWAPPABLE_HOOKS.HOOK_SYS_STDOUT)
    stdout_handler.setLevel(consolelevel)
    stdout_handler.addFilter(LessThanRecordFilter(logging.WARNING))

    stderr_handler = logging.StreamHandler(SWAPPABLE_HOOKS.HOOK_SYS_STDERR)
    stderr_handler.setLevel(consolelevel)
    stderr_handler.addFilter(GreaterOrEqualRecordFilter(logging.WARNING))

    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(stderr_handler)


    for binfo in log_branches:
        try:
            logger_name = binfo["name"]
            logfilename = binfo["logname"]
            log_level = binfo["loglevel"]

            logging_create_branch_logger(logger_name, logfilename, log_level)
        except Exception: # pylint: disable=broad-except
            errmsg = "Error configuration branch logger." + os.linesep
            errmsg = traceback.format_exc()
            root_logger.error(errmsg)

    logger = logging.getLogger()

    if consolelevel != LogLevel.QUIET.name:
        logger.section("Logging Initialized")

    return rel_logfilename

