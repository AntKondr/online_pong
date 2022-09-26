import socket
from random import randint
from time import sleep


class Player():
    def __init__(self, socket, adres, side):
        self.socket = socket
        self.adres = adres
        self.side = side
        self.request = None


def load_response(request_text):
    global left_rocket_y
    global right_rocket_y
    global run
    if request_text == 'start parameters':
        return f'{ball_x};{ball_y};{direct_ball_x};{direct_ball_y}'

    elif request_text == 'second player':
        if len(players) == 2:
            return 'True'
        else:
            return 'False'

    elif request_text == 'coords left rocket':
        return f'{left_rocket_y}'

    elif request_text == 'coords right rocket':
        return f'{right_rocket_y}'

    elif request_text == 'a':
        left_rocket_y -= 1
        return f'{right_rocket_y}'
    elif request_text == 'z':
        left_rocket_y += 1
        return f'{right_rocket_y}'

    elif request_text == 'k':
        right_rocket_y -= 1
        return f'{left_rocket_y}'
    elif request_text == 'm':
        right_rocket_y += 1
        return f'{left_rocket_y}'

    elif request_text == 'left is looser':
        run = False
    elif request_text == 'right is looser':
        run = False


lan_ip = '192.168.1.107'
local_ip = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((local_ip, 8000))
server_socket.setblocking(False)
server_socket.listen()

with open('who_loose', 'r') as file:
    looser = file.read()
direct = (-1, 1)
if looser == 'right':
    ball_x, ball_y = (3, 14)
    direct_ball_x = direct[1]
else:
    ball_x, ball_y = (116, 14)
    direct_ball_x = direct[0]
direct_ball_y = direct[randint(0, 1)]

left_rocket_y = 14
right_rocket_y = 14

rooms = []
players = []
run = True
while run:
    try:
        client_socket, client_adres = server_socket.accept()
        client_socket.setblocking(False)
        new_player = Player(client_socket, client_adres, 'left')
        players.append(new_player)
    except:
        pass
    for player in players:
        try:
            player.request = player.socket.recv(128).decode('utf-8')
            print('request =>', player.request)
        except:
            pass
        try:
            response = load_response(player.request)
            player.socket.send(response.encode('utf-8'))
        except:
            pass
        player.request = None
    sleep(0.05)