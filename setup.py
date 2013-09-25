import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('GuildViewer.py', base=base)
]

setup(name='GuildViewer',
      version='0.1',
      description='GuildViewer script',
      executables=executables
      )
