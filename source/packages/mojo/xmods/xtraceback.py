"""
.. module:: xtraceback
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains functions for enhancing and formatting exceptions and
               common exception types not provided by python.

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

import inspect
import os
import traceback

from mojo.xmods.xformatting import split_and_indent_lines

MEMBER_TRACE_POLICY = "__traceback_format_policy__"

class TracebackFormatPolicy:
    Brief = "Brief"
    Full = "Full"
    Hide = "Hide"

VALID_MEMBER_TRACE_POLICY = ["Brief", "Full", "Hide"]


class TRACEBACK_CONFIG:
    TRACEBACK_POLICY_OVERRIDE = None
    TRACEBACK_MAX_FULL_DISPLAY = 5

class EnhancedErrorMixIn:
    def __init__(self, *args, **kwargs):
        self._context = {}
        return

    @property
    def context(self):
        return self._context

    def add_context(self, content, label="CONTEXT"):
        """
            Adds context to an exception and associates it with the function context
            on the stack.
        """
        caller_stack = inspect.stack()[2]
        caller_func_name = caller_stack.frame.f_code.co_name

        self._context[caller_func_name] = {
            "label": label,
            "content": content
        }

        return


def collect_stack_frames(calling_frame, ex_inst):

    max_full_display = TRACEBACK_CONFIG.TRACEBACK_MAX_FULL_DISPLAY

    last_items = None
    tb_code = None
    tb_lineno = None

    tb_frames = []

    for tb_frame, tb_lineno in traceback.walk_stack(calling_frame):
        tb_frames.insert(0, (tb_frame, tb_lineno))
        if tb_frame.f_code.co_name == '<module>':
            break 

    tb_frames.pop()

    for tb_frame, tb_lineno in traceback.walk_tb(ex_inst.__traceback__):
        tb_frames.append((tb_frame, tb_lineno))

    tb_frames.reverse()

    traceback_list = []

    for tb_frame, tb_lineno in tb_frames:
        tb_code = tb_frame.f_code
        co_filename: str = tb_code.co_filename
        co_name: str = tb_code.co_name
        co_arg_names = tb_code.co_varnames[:tb_code.co_argcount]
        co_argcount = tb_code.co_argcount
        co_locals = tb_frame.f_locals

        co_format_policy = TracebackFormatPolicy.Brief

        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is None:
            co_module = inspect.getmodule(tb_code)
            if co_module and hasattr(co_module, MEMBER_TRACE_POLICY):
                cand_format_policy = getattr(co_module, MEMBER_TRACE_POLICY)
                if cand_format_policy in VALID_MEMBER_TRACE_POLICY:
                    co_format_policy = cand_format_policy
        else:
            co_format_policy = TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE

        items = [co_filename, tb_lineno, co_name, "", None]
        if last_items is not None:
            code_args = []
            for argidx in range(0, co_argcount):
                argname = co_arg_names[argidx]
                argval = co_locals[argname]
                code_args.append("%s=%r" % (argname, argval))

            last_items[-2] = "%s(%s)" % (co_name, ", ".join(code_args)) # pylint: disable=unsupported-assignment-operation

        last_items = items

        traceback_list.append(items)
        last_items = items

        if max_full_display > 0 and co_format_policy == TracebackFormatPolicy.Full \
            and os.path.exists(co_filename) and co_filename.endswith(".py"):
            context_lines, context_startline = inspect.getsourcelines(tb_code)
            context_lines = [cline.rstrip() for cline in context_lines]
            clindex = (tb_lineno - context_startline)
            last_items[-2] = context_lines[clindex].strip()
            last_items[-1] = context_lines
            max_full_display -= 1

    return traceback_list


def enhance_exception(xcpt: BaseException, content, label="CONTEXT"):
    """
        Allows for the enhancing of exceptions.
    """

    # EnhancedErrorMixIn just uses Duck typing so it should be safe to dynamically
    # append any exception that does not already inherit include EnhancedErrorMixIn
    # in its base clases list.
    xcpt_type = type(xcpt)

    if EnhancedErrorMixIn not in xcpt_type.__bases__:
        xcpt_type.__bases__ += (EnhancedErrorMixIn,)
        xcpt._context = {}

    xcpt.add_context(content, label=label)

    return


def format_exc_lines():
    """
        Gets a 'format_exc' result and splits it into mutliple lines.
    """
    rtn_lines = traceback.format_exc().splitlines()
    return rtn_lines


def format_exception(ex_inst: BaseException):

    etypename = type(ex_inst).__name__
    eargs = ex_inst.args

    exmsg_lines = [
        "%s: %s" % (etypename, repr(eargs).rstrip(",")),
        "TRACEBACK (most recent call last):"
    ]

    previous_frame = inspect.currentframe().f_back

    stack_frames = collect_stack_frames(previous_frame, ex_inst)
    stack_frames_len = len(stack_frames)

    for co_filename, co_lineno, co_name, co_code, co_context in stack_frames:

        exmsg_lines.extend([
            '  File "%s", line %d, in %s' % (co_filename, co_lineno, co_name),
            "    %s" % co_code
        ])

        if hasattr(ex_inst, "context") and co_name in ex_inst.context:
            cxtinfo = ex_inst.context[co_name]
            exmsg_lines.append('    %s:' % cxtinfo["label"])
            exmsg_lines.extend(split_and_indent_lines(cxtinfo["content"], 2, indent=3))

        if co_context is not None and len(co_context) > 0 and stack_frames_len > 1:
            exmsg_lines.append('    CODE:')
            firstline = co_context[0]
            lstrip_len = len(firstline) - len(firstline.lstrip())
            co_context = [cline[lstrip_len:] for cline in co_context]
            co_context = ["      %s" % cline for cline in co_context]
            exmsg_lines.extend(co_context)
        exmsg_lines.append('')

    return exmsg_lines

