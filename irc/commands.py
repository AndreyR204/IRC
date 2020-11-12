import socket
import re
import irc.const as const
import abc


class ClientCommand(abc.ABC):
    usage: str
    arg = False

    def __init__(self, client):
        self._client = client
        self._args = None
        self.output = None

    def get_args(self):
        if self.arg:
            self._args = input(self.usage+":")

    @abc.abstractmethod
    def execute(self, *args):
        pass

    def __call__(self) -> str:
        self.get_args()
        if self.arg:
            result = self.execute(self._args)
            return result + "\r\n" if result else ""
        return ""


class PartCommand(ClientCommand):
    usage = ""
    arg = False

    def execute(self) -> str:
        ch_name = self._client.current_channel
        self._client.current_channel = None
        self._client.joined_channels.remove(ch_name)
        return f"PART {ch_name}"


class ListCommand(ClientCommand):
    usage = ""
    arg = False

    def execute(self) -> str:
        return "LIST"


class NamesCommand(ClientCommand):
    usage = ""
    arg = False

    def execute(self) -> str:
        return f"NAMES {self._client.current_channel}"


class PrivateMessageCommand(ClientCommand):
    usage = "TARGET TEXT"
    arg = True

    def execute(self, target: str, *message) -> str:
        return f"PRIVMSG {target} :{' '.join(message)}"


class JoinCommand(ClientCommand):
    usage = "CHANNEL [PASSWORD]"
    arg = True

    def execute(self, ch_name: str, password="") -> str:
        ch_name = ch_name.lower()
        self._client.current_channel = ch_name
        self._client.joined_channels.add(ch_name)

        if not self._client.is_connected:
            self.output = "Прежде чем вводить данную команду, подключитесь к серверу!"
            return ""

        ch_name = self._args[0].lower()
        if ch_name in self._client.joined_channels:
            self.output = "Вы уже присоединились к данному каналу!"
            return ""
        return f"JOIN {ch_name} {password}"


class NickCommand(ClientCommand):
    NICK_EXPR = re.compile(r"^[a-zA-Zа-я-А-Я][\w]+")
    usage = "NICKNAME"
    arg = True

    def execute(self, new_nickname: str) -> str:
        self._client.prev_nick = self._client.username
        self._client.username = new_nickname

        new_nickname = self._args[0]
        if not self.NICK_EXPR.search(new_nickname):
            self.output = "Недопустимый никнейм!"
            return ""
        return f"NICK {new_nickname}"


class DisconnectCommand(ClientCommand):
    usage = "/quit"
    arg = False

    def execute(self) -> None:
        if not self._client.is_connected:
            self.output = "Прежде чем вводить данную команду, подключитесь к серверу!"
        else:
            self._client.hostname = None
            self._client.is_connected = False
            self._client.joined_channels = set()
            self._client.current_channel = None
            self._client.conn.shutdown(socket.SHUT_WR)
            self.output = f"Отключение от сервера..."


class SwitchCommand(ClientCommand):
    usage = "CHANNEL"
    arg = True

    def execute(self, ch_name: str) -> None:
        ch_name = ch_name.lower()
        if ch_name in self._client.joined_channels and ch_name != self._client.current_channel:
            self.output = f"Переключение текущего канала на {ch_name}..."
            self._client.current_channel = ch_name
        else:
            self.output = f"Вы не присоединены к каналу {ch_name}!"


class HelpCommand(ClientCommand):
    usage = "/help"
    arg = False

    def execute(self) -> None:
        self.output = const.HELP_MESSAGE


class ConnectCommand(ClientCommand):
    usage = "HOSTNAME [PORT]"
    arg = True

    def execute(self, hostname: str, port=6667) -> str:
        if self._client.is_connected:
            self.output = "Вы уже подключены к серверу!"
            return ""
        self._client.conn = socket.socket()
        self._client.conn.settimeout(10)
        try:
            self._client.conn.connect((hostname, port))
        except socket.gaierror as e:
            self.output = f"Не удалось подключиться по заданному адресу: {hostname}"
            return ""

        self._client.conn.settimeout(None)
        self._client.hostname = hostname
        self._client.is_connected = True
        return f"NICK {self._client.username}\r\nUSER 1 1 1 1"


class CodePageCommand(ClientCommand):
    usage = "ENCODING"
    arg = True

    def execute(self, code_page: str) -> str:
        code_page = self._args[0].lower()
        if code_page not in const.CODE_PAGES:
            self.output = f"Допустимые кодировки: {const.CODE_PAGES}"
            return ""
        self._client.code_page = code_page
        self.output = f"Текущая кодировка изменена на {code_page}"
        return ""


class AddToFavCommand(ClientCommand):
    usage = "/add"
    arg = False

    def execute(self) -> None:
        self._client.favourites.add(self._client.hostname)
        self.output = f"Сервер {self._client.hostname} добавлен в список избранных"


class ShowFavCommand(ClientCommand):
    usage = "/fav"
    arg = False

    def execute(self) -> None:
        servers = []
        for server in self._client.favourites:
            servers.append(server)
        self.output = "Список серверов в избранном:\n" + "\n".join(servers)


class ExitCommand(ClientCommand):
    usage = "/exit"
    arg = False

    def execute(self) -> None:
        print("Exiting application")
        self._client.is_working = False
        if self._client.is_connected:
            self._client.is_connected = False
            self._client.conn.shutdown(socket.SHUT_WR)
        exit()
