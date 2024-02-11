
from typing import Optional, Type

from types import TracebackType

import tempfile
import os
import shutil

class AutoCleanDirectoryScope:

    def __init__(self, directory: str):
        self._directory = directory
        return
    
    def __enter__(self) -> "AutoCleanDirectoryScope":
        return self
    
    def __exit__(self, ex_type: Type[BaseException], ex_inst: BaseException, ex_tb: TracebackType) -> bool:
        shutil.rmtree(self._directory, ignore_errors=True)
        return False
    
class AutoCleanFileScope:

    def __init__(self, filename: str):
        self._filename = filename
        return
    
    def __enter__(self) -> "AutoCleanFileScope":
        return self
    
    def __exit__(self, ex_type: Type[BaseException], ex_inst: BaseException, ex_tb: TracebackType) -> bool:
        os.remove(self._filename)
        return False

def create_autoclean_directory_scope(directory: str) -> AutoCleanDirectoryScope:
    scope = AutoCleanDirectoryScope(directory)
    return scope

def create_autoclean_file_scope(filename: str) -> AutoCleanFileScope:
    scope = AutoCleanFileScope(filename)
    return scope

def create_autoclean_tempdir_scope(suffix: Optional[str] = None, prefix: Optional[str] = None,
                                   dir: Optional[str] = None) -> AutoCleanDirectoryScope:
    tmpdir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
    scope = AutoCleanDirectoryScope(tmpdir)
    return scope

def create_autoclean_tempfile_scope(suffix: Optional[str] = None, prefix: Optional[str] = None,
                                   dir: Optional[str] = None) -> AutoCleanFileScope:
    tmpfile = tempfile.mktemp(suffix=suffix, prefix=prefix, dir=dir)
    scope = AutoCleanFileScope(tmpfile)
    return scope
