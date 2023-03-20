
from typing import Union, Type

from types import TracebackType

from threading import Lock, RLock

class LockedScope:

    def __init__(self, lock: Union[Lock, RLock]):
        self._lock = lock
        return
    
    def __enter__(self) -> "LockedScope":
        self._lock.acquire()
        return self

    def __exit__(self, ex_type: Type[BaseException], ex_inst: BaseException, ex_tb: TracebackType) -> bool:
        self._lock.release()
        return False

class UnLockedScope:

    def __init__(self, lock: Union[Lock, RLock]):
        self._lock = lock
        return
    
    def __enter__(self) -> "UnLockedScope":
        self._lock.release()
        return self

    def __exit__(self, ex_type: Type[BaseException], ex_inst: BaseException, ex_tb: TracebackType) -> bool:
        self._lock.acquire()
        return False

def create_locked_scope(lock: Union[Lock, RLock]):

    lkscope = LockedScope(lock)

    return lkscope

def create_unlocked_scope(lock: Union[Lock, RLock]):

    unlkscope = UnLockedScope(lock)

    return unlkscope