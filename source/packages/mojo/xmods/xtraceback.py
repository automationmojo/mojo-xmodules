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

from typing import Any, Dict, List, Tuple

import dis
import inspect
import os
import traceback

from dataclasses import dataclass, asdict

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
    TRACEBACK_EXPAND_FIRST_N = 1


@dataclass
class OriginDetail:
    file: str
    lineno: int
    scope: str

@dataclass
class TraceDetail:
    origin: str
    call: str
    code: List[str]
    context: Dict[str, List[str]]

@dataclass
class TracebackDetail:
    extype: str
    exargs: List[str]
    traces: List[TraceDetail]

def is_field(candidate):

    if inspect.ismodule(candidate):
        return False
    if inspect.isclass(candidate):
        return False
    if inspect.isfunction(candidate):
        return False
    if inspect.isgeneratorfunction(candidate):
        return False
    if inspect.isgenerator(candidate):
        return False
    if inspect.iscoroutinefunction(candidate):
        return False
    if inspect.iscoroutine(candidate):
        return False
    if inspect.isasyncgenfunction(candidate):
        return False
    if inspect.isasyncgen(candidate):
        return False
    if inspect.istraceback(candidate):
        return False
    if inspect.isframe(candidate):
        return False
    if inspect.iscode(candidate):
        return False
    if inspect.isbuiltin(candidate):
        return False
    if inspect.isroutine(candidate):
        return False
    if inspect.isabstract(candidate):
        return False
    if inspect.ismethoddescriptor(candidate):
        return False
    if inspect.isdatadescriptor(candidate):
        return False
    if inspect.isgetsetdescriptor(candidate):
        return False
    if inspect.ismemberdescriptor(candidate):
        return False
    return True

def get_public_field_members(obj) -> List[Tuple[str, Any]]:
    public_members = []

    members: List[Tuple[str, Any]] = inspect.getmembers(obj, is_field)

    for mname, minst in members:
        if mname[0] != "_":
            public_members.append((mname, minst))

    return public_members

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
    expand_first_n = TRACEBACK_CONFIG.TRACEBACK_EXPAND_FIRST_N

    last_items = None
    last_co_name = None
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

            last_items[-2] = "%s(%s)" % (last_co_name, ", ".join(code_args)) # pylint: disable=unsupported-assignment-operation

        last_items = items
        last_co_name = co_name

        traceback_list.append(items)
        last_items = items

        if expand_first_n > 0 or (max_full_display > 0 and co_format_policy == TracebackFormatPolicy.Full):
            if os.path.exists(co_filename) and co_filename.endswith(".py"):
                context_lines, context_startline = inspect.getsourcelines(tb_code)
                context_lines = [cline.rstrip() for cline in context_lines]
                clindex = (tb_lineno - context_startline)
                last_items[-2] = context_lines[clindex].strip()
                last_items[-1] = context_lines
                max_full_display -= 1
                expand_first_n -= 1

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
        "%s: %s" % (etypename, repr(eargs)),
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
            firstline = co_context[0]
            lstrip_len = len(firstline) - len(firstline.lstrip())
            co_context = [cline[lstrip_len:] for cline in co_context]
            co_context = ["      %s" % cline for cline in co_context]
            exmsg_lines.extend(co_context)

        exmsg_lines.append('')

    return exmsg_lines

def create_traceback_detail(ex_inst: BaseException) -> TracebackDetail:

    etypename = type(ex_inst).__name__
    eargs = [repr(a) for a in ex_inst.args]
    etraces = []

    previous_frame = inspect.currentframe().f_back

    stack_frames = collect_stack_frames(previous_frame, ex_inst)
    stack_frames_len = len(stack_frames)

    for co_filename, co_lineno, co_name, co_code, co_context in stack_frames:
        ntfile = OriginDetail(file=co_filename, lineno=co_lineno, scope=co_name)
        ntcall = co_code
        ntcode = []
        ntcontext = {}

        if co_context is not None and len(co_context) > 0 and stack_frames_len > 1:
            firstline = co_context[0]
            lstrip_len = len(firstline) - len(firstline.lstrip())
            ntcode = [cline[lstrip_len:] for cline in co_context]

        if hasattr(ex_inst, "context") and co_name in ex_inst.context:
            ntcontext = ex_inst.context[co_name]

        nttrace = TraceDetail(origin=ntfile, call=ntcall, code=ntcode, context=ntcontext)
        etraces.append(nttrace)

    tb_detail = TracebackDetail(extype=etypename, exargs=eargs, traces=etraces)

    return tb_detail

