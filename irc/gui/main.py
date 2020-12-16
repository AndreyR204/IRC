from PyQt5.QtWidgets import QApplication
import sys
import irc.__main__ as main
from irc.gui.mydesign import ClientWindow
from irc.client import Client

if __name__ == "__main__":
    app = QApplication([])
    config = main.get_config()
    client = Client(config["Settings"]["nickname"],
                    config["Settings"]["codepage"],
                    set(config["Servers"].keys()))
    main_window = ClientWindow(client)
    main_window.setup_ui()
    main_window.show()
    sys.exit(app.exec())
    main.refresh_config()
