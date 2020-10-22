#IRC Client
Простой IRC клиент для командной строки или использования в составе сторонней программы.
## Install
git clone https://github.com/AndreyR204/IRC.git 
pip install -r requirements.txt
## Usage
usage: main.py [-h] [--server SERVER] [--port PORT] [--username USERNAME]
               --channel CHANNEL

optional arguments:
  -h, --help            show this help message and exit
  --server SERVER, -s SERVER
                        Server you like to connect
  --port PORT, -p PORT  Server port
  --username USERNAME, -u USERNAME
                        Your username
  --channel CHANNEL, -c CHANNEL
                        Channel you like to join
