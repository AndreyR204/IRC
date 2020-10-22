#!/usr/bin/env python3
import argparse
import configparser
from pathlib import Path
from IRC import app

server = ''
port = ''
username = ''
channel = ''
config = configparser.ConfigParser()
config['MAIN'] = {}
if not Path('conf.ini').is_file():
    config['MAIN']['server'] = input('Enter server address: ')
    config['MAIN']['port'] = input('Enter server port: ')
    config['MAIN']['username'] = input('Enter your username: ')
    with open('conf.ini', 'w') as configfile:
        config.write(configfile)
config.read('conf.ini')
parser = argparse.ArgumentParser()
parser.add_argument('--server', '-s', default=config['MAIN']['server'], help='Server you like to connect')
parser.add_argument('--port', '-p', default=config['MAIN']['port'], help='Server port')

parser.add_argument('--username', '-u', default=config['MAIN']['username'], help='Your username')
parser.add_argument('--channel', '-c', help='Channel you like to join', required=True)
args = parser.parse_args()
config['MAIN']['server'] = args.server
config['MAIN']['port'] = args.port
config['MAIN']['username'] = args.username
with open('conf.ini', 'w') as configfile:
    config.write(configfile)
app.do_chatting(args.channel)


