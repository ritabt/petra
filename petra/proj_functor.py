from typing import cast, Callable

import subprocess
import petra as pt
import unittest

from ctypes import CFUNCTYPE, c_int32

program = pt.Program("module")
