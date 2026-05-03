from database.db import initialize
from gui.app import App


def main():
    initialize()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
