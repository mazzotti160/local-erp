import sys
import os

# Suppress console window in development (PyInstaller handles this via --noconsole)
if not getattr(sys, "frozen", False) and sys.executable.lower().endswith("python.exe"):
    import subprocess
    pythonw = sys.executable[:-10] + "pythonw.exe"
    if os.path.exists(pythonw):
        subprocess.Popen([pythonw] + sys.argv)
        sys.exit()

from gui.setup import run_setup_if_needed
from database.db import initialize
from gui.app import App


def main():
    run_setup_if_needed()
    initialize()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
