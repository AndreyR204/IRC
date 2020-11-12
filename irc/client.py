import keyboard
import socket
import threading
from irc import commands as com
from irc import messages as msg
import irc.const as const


class Client:

    def __init__(self, username, code, favourites):
        self.username = username
        self.channel = None
        self.code = code
        self.hostname = None
        self.joined_channels = set()
        self.is_connected = False
        self.is_working = True
        self.favourites = favourites
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_handler = CommandHandler(self)

    def cmd_prompt(self):
        if not self.channel:
            return f"<{self.username}>: "
        return f"[{self.channel}] <{self.username}>: "

    def start_client(self) -> None:
        input_thread = threading.Thread(target=self.wait_for_input)
        input_thread.start()
        self.wait_for_response()
        input_thread.join()

    def wait_for_input(self) -> None:
        while self.is_working:
            command = self.command_handler.get_text(input(self.cmd_prompt()))
            execution_result = command().encode(self.code)
            if self.is_connected:
                self.conn.sendall(execution_result)
            if command.output:
                print(command.output)

    def wait_for_response(self) -> None:
        handler = MessageHandler(self)
        while self.is_working:
            while self.is_connected:
                data = self.conn.recv(const.BUFFER_SIZE)
                print(handler.parse_response(data))


class CommandHandler:
    def __init__(self, client: Client):
        self._client = client
        self.commands = {
            "/c": com.CodePageCommand,
            "/n": com.NickCommand,
            "/h": com.HelpCommand,
            "/f": com.ShowFavCommand,
            "/s": com.ConnectCommand,
            "/e": com.ExitCommand,
            "/p": com.PrivateMessageCommand,
            "/a": com.AddToFavCommand,
            "/j": com.JoinCommand,
            "/l": com.ListCommand,
            "/ns": com.NamesCommand,
            "/lv": com.PartCommand,
            "/q": com.DisconnectCommand,
            "/sw": com.SwitchCommand,
        }

    def get_text(self, input_text: str):
        if input_text.startswith("/"):
            if input_text in self.commands:
                return self.commands[input_text](self._client)


class MessageHandler:
    def __init__(self, client: Client):
        self.client = client
        self.messages = {
            "JOIN": msg.JoinMessage,
            "PART": msg.PartMessage,
            "NICK": msg.NickMessage,
            "MODE": msg.ModeMessage,
            "PRIVMSG": msg.PrivateMessage,
            "NOTICE": msg.NoticeMessage
        }

    def get_messages(self, decoded_data: str):
        for line in decoded_data.split("\r\n"):
            words = line.split(" ")
            command_name = words[1].upper()
            if command_name in self.messages:
                yield self.messages[command_name](self.client, line)
            elif command_name.isdigit():
                yield msg.ServiceMessage(self.client, line)
        return ""

    def parse_response(self, data: bytes) -> str:
        decoded_data = data.decode(self.client.code)
        result = [str(message) for message in self.get_messages(decoded_data)]
        return "\n".join(result)
