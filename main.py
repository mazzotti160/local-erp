import sys
import os
import subprocess

# Relaunch with pythonw (no console) if running with python.exe
if sys.executable.lower().endswith("python.exe"):
    pythonw = sys.executable[:-10] + "pythonw.exe"
    if os.path.exists(pythonw):
        subprocess.Popen([pythonw] + sys.argv)
        sys.exit()

from database.db import initialize
from gui.app import App


def main():
    initialize()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
