from PyQt5.QtWidgets import QApplication
import sys
import irc.__main__ as mn
import irc.gui.design as design
from irc.client import Client

if __name__ == "__main__":
    app = QApplication([])
    config = mn.get_config()
    client = Client(config["Settings"]["nickname"],
                    config["Settings"]["codepage"],
                    set(config["Servers"].keys()))
    main_window = design.Ui_ClientWindow(client)
    main_window.setup_ui(main_window)
    main_window.show()
    app.exec()
    sys.exit(mn.refresh_config(client))
