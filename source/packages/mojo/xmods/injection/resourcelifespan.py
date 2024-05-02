__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []



import enum

class ResourceLifespan(str, enum.Enum):
    Session = "session"
    Package = "package"
    Test = "test"
    Task = "task"
