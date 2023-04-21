"""
.. module:: pipedprocess
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

from typing import Any, Callable, Iterable, Mapping, Optional

import os
import sys
import threading

from io import StringIO
from multiprocessing import Process, Queue

class RemoteStdTee(StringIO):
    def __init__(self, queue: Queue, orig_file):
        super().__init__()
        self._pid = os.getpid()
        self._queue = queue
        self._orig_file = orig_file
        return
    
    def flush(self):
        buffer = self.getvalue()
        if len(buffer) > 0:
            self._queue.put(f"[{self._pid}] {buffer}{os.linesep}")
        self.truncate()
        return self._orig_file.flush()

    def write(self, s):
        nlidx = s.find(os.linesep)
        if nlidx < 0:
            StringIO.write(self, s)
        else:
            nlidx = s.rindex(os.linesep)
            rems = s[nlidx + 1:]
            qmsg = self.getvalue() + s[:nlidx]
            self.seek(0)
            self.truncate()
            if len(rems) > 0:
                StringIO.write(self, rems)
            self._queue.put(f"[{self._pid}] {qmsg}{os.linesep}")
        return self._orig_file.write(s)


def piped_process_main(entry_point: Callable, stdout_queue: Queue, stderr_queue: Queue, *args):
    sys.stdout = RemoteStdTee(stdout_queue, sys.__stdout__)
    sys.stderr = RemoteStdTee(stderr_queue, sys.__stderr__)
    entry_point(*args)
    return


class PipedProcess(Process):

    def __init__(self, group: None = None, target: Optional[Callable]=None, name: Optional[str]=None, args: Iterable[Any] = (),
                 kwargs: Mapping[str, Any] = {}, *, daemon: Optional[bool]=None) -> None:
        
        self._stdout_queue = Queue()
        self._stderr_queue = Queue()

        self._stdout_thread = threading.Thread(target=self.stdout_monitor, daemon=True)
        self._stdout_thread.start()

        self._stderr_thread = threading.Thread(target=self.stderr_monitor, daemon=True)
        self._stderr_thread.start()

        rmtarget = piped_process_main
        rmargs = target, self._stdout_queue, self._stderr_queue, *args
        super().__init__(group=group, target=rmtarget, name=name, args=rmargs, kwargs=kwargs, daemon=daemon)
        return
    
    def stdout_monitor(self):

        try:
            while True:
                s = self._stdout_queue.get()
                sys.stdout.write(s)
        except:
            pass

        return
    
    def stderr_monitor(self):
        
        try:
            while True:
                s = self._stderr_queue.get()
                sys.stderr.write(s)
        except:
            pass
        
        return
    



