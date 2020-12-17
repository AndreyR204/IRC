# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from irc.client import Client, MessageHandler
import threading
from irc import const


class Ui_ClientWindow(QtWidgets.QMainWindow):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client

    def setup_ui(self, ClientWindow):
        ClientWindow.setObjectName("ClientWindow")
        ClientWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.Send = QtWidgets.QPushButton(self.centralwidget)
        self.Send.setObjectName("Send")
        self.gridLayout.addWidget(self.Send, 1, 0, 1, 1)
        self.Help = QtWidgets.QPushButton(self.centralwidget)
        self.Help.setObjectName("Help")
        self.gridLayout.addWidget(self.Help, 1, 2, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setUndoRedoEnabled(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 3)
        ClientWindow.setCentralWidget(self.centralwidget)
        self.Send.clicked.connect(self.send_user_input)
        self.Help.clicked.connect(self.send_user_input)
        self.chat = self.textEdit

        self.retranslateUi(ClientWindow)
        QtCore.QMetaObject.connectSlotsByName(ClientWindow)
        out_thread = threading.Thread(target=self.get_out)
        out_thread.start()

    def get_out(self):
        client = self.client
        handler = MessageHandler(self, client)
        while self.client.is_working:
            while self.client.is_connected:
                data = self.client.sock.recv(const.BUFFER_SIZE)
                self.chat.append(handler.parse_response(data))

    def send_user_input(self):
        text = self.lineEdit.text()
        if text.strip():
            command = self.client.command_handler.get_command(text)
            input_text = f"<{self.client.nickname}>: {text}"
            self.chat.append(input_text)
            execution_result = command().encode(self.client.code_page)
            if self.client.is_connected:
                self.client.sock.sendall(execution_result)
            if command.output:
                self.chat.append(command.output)
            self.lineEdit.clear()

    def retranslateUi(self, ClientWindow):
        _translate = QtCore.QCoreApplication.translate
        ClientWindow.setWindowTitle(_translate("ClientWindow", "IRC"))
        self.Send.setText(_translate("ClientWindow", "Send"))
        self.Help.setText(_translate("ClientWindow", "Help"))
        self.Send.setShortcut(_translate("ClientWindow", "Return"))
