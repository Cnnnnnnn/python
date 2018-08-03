import sys
from cx_Freeze import setup, Executable
from cx_Freeze.windist import *

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {'packages': [], 'excludes': []}

setup(  name = 'teat',
        version = '1.0',
        description = 'test',
        options = {'build_exe': build_exe_options},
        executables = [Executable('runtest.py')])