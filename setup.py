import os.path
import sys
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter", "pyglet", "shutil", "sys", "time", "random", "vlc", "backend"],
                     "excludes": [],
                     "include_files": ['backend.py',
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                       'bitmaps/player_play.png', 'bitmaps/player_pause.png',
                                       'bitmaps/player_next.png', 'bitmaps/player_ff.png',
                                       'bitmaps/player_rev.png', 'bitmaps/shuffle.png'
                                       ]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Avideom",
        version = "0.1",
        description = "Avideom",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui.py", base=base)])