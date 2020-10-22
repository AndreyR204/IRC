import socket
import threading
import sys
import configparser


def channel(channel):
    if not channel.startswith("#"):
        return "#" + channel
    return channel


def print_response(client):
    resp = client.get_response()
    if resp:
        msg = resp.strip().split(":")
        print("< {}> {}".format(msg[1].split("!")[0], msg[2].strip()))


class IRCSimpleClient:

    def __init__(self, username, channel, server, port):
        self.username = username
        self.server = server
        self.port = int(port)
        self.channel = channel

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    def get_response(self):
        return self.conn.recv(512).decode("utf-8")

    def send_cmd(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message).encode("utf-8")
        self.conn.send(command)

    def send_message_to_channel(self, message):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.send_cmd(command, message)

    def join_channel(self):
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)


def do_chatting(channel):
    config = configparser.ConfigParser()
    config.read('conf.ini')
    username = config['MAIN']['username']
    server = config['MAIN']['server']
    port = config['MAIN']['port']
    cmd = ""
    joined = False
    client = IRCSimpleClient(username, channel, server, port)
    client.connect()

    while not joined:
        resp = client.get_response()
        print(resp.strip())
        if "No Ident response" in resp:
            client.send_cmd("NICK ", username)
            client.send_cmd(
                "USER ", "{} * * :{}".format(username, username))

        if "376" in resp:
            client.join_channel()

        if "433" in resp:
            username = "_" + username
            client.send_cmd("NICK ", username)
            client.send_cmd(
                "USER ", "{} * * :{}".format(username, username))

        if "PING" in resp:
            client.send_cmd("PONG ", ":" + resp.split(":")[1])

        if "366" in resp:
            joined = True

    while cmd != "/quit":
        cmd = input("< {}> ".format(username)).strip()
        if cmd == "/quit":
            client.send_cmd("QUIT ", "Good bye!")
        client.send_message_to_channel(cmd)

        response_thread = threading.Thread(target=print_response)
        response_thread.daemon = True
        response_thread.start()
