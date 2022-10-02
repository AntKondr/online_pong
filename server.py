import socket
from random import randint
from time import sleep


class Player:
    def __init__(self, socket, adres):
        self.socket = socket
        self.adres = adres
        self.request = None


class Room:
    sides = ('l', 'r')
    directs = (-1, 1)
    left_rocket_x = 2
    right_rocket_x = 117

    def __init__(self, pair_players, room_id):
        self.pair_players = pair_players
        self.left_player = self.pair_players[0]
        self.right_player = self.pair_players[1]
        self.id = room_id
        self.round = 1
        self.left_rocket_y = 14
        self.right_rocket_y = 14

    def set_start_parameters(self):
        serving_side = Room.sides[randint(0, 1)]
        if serving_side == 'l':
            self.ball_x, self.ball_y = (3, self.left_rocket_y)
            self.direct_ball_x = Room.directs[1]
        else:
            self.ball_x, self.ball_y = (116, self.right_rocket_y)
            self.direct_ball_x = Room.directs[0]
        self.direct_ball_y = Room.directs[randint(0, 1)]

    def move_ball(self):
        if self.ball_x == (Room.right_rocket_x - 1) and ((self.ball_y == self.right_rocket_y) or (self.ball_y == self.right_rocket_y + 1) or (self.ball_y == self.right_rocket_y - 1)):
            self.direct_ball_x = -1
        elif self.ball_x == (Room.left_rocket_x + 1) and ((self.ball_y == self.left_rocket_y) or (self.ball_y == self.left_rocket_y + 1) or (self.ball_y == self.left_rocket_y - 1)):
            self.direct_ball_x = 1

        if self.ball_y == 28:
            self.direct_ball_y = -1
        elif self.ball_y == 1:
            self.direct_ball_y = 1

        self.ball_x += self.direct_ball_x
        self.ball_y += self.direct_ball_y

    def form_response(self, request):
        if request == 'a':
            self.left_rocket_y -= 1
            return f'{self.right_rocket_y};{self.ball_x};{self.ball_y}'
        elif request == 'z':
            self.left_rocket_y += 1
            return f'{self.right_rocket_y};{self.ball_x};{self.ball_y}'

        elif request == 'k':
            self.right_rocket_y -= 1
            return f'{self.left_rocket_y};{self.ball_x};{self.ball_y}'
        elif request == 'm':
            self.right_rocket_y += 1
            return f'{self.left_rocket_y};{self.ball_x};{self.ball_y}'

        elif request == 'coords left rocket':
            return f'{self.left_rocket_y};{self.ball_x};{self.ball_y}'

        elif request == 'coords right rocket':
            return f'{self.right_rocket_y};{self.ball_x};{self.ball_y}'

        elif request == 'start parameters':
            return f'{self.ball_x};{self.ball_y};{self.direct_ball_x};{self.direct_ball_y}'

        elif request == 'left is looser':
            self.set_start_parameters()
            return f'{self.ball_x};{self.ball_y};{self.direct_ball_x};{self.direct_ball_y}'
        elif request == 'right is looser':
            self.set_start_parameters()
            return f'{self.ball_x};{self.ball_y};{self.direct_ball_x};{self.direct_ball_y}'


lan_ip1 = '192.168.43.201'
lan_ip2 = '192.168.1.107'
local_ip = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((local_ip, 8000))
server_socket.setblocking(False)
server_socket.listen()

rooms = []
room_id = 1
pair_players = []
run = True
while run:
    try:
        client_socket, client_adres = server_socket.accept()
        client_socket.setblocking(False)
        new_player = Player(client_socket, client_adres)
        pair_players.append(new_player)
    except:
        pass
    if len(pair_players) == 2:
        new_room = Room(pair_players, room_id)
        new_room.set_start_parameters()
        rooms.append(new_room)
        room_id += 1
        for player in pair_players:
            player.socket.send('Go'.encode('utf-8'))
        pair_players = []

    if len(rooms) > 0:
        for room in rooms:
            print('i am in', room.id, 'room')
            for player in room.pair_players:
                try:
                    player.request = player.socket.recv(128).decode('utf-8')
                    print('request =>', player.request)
                except:
                    pass
                try:
                    response = room.form_response(player.request)
                    player.socket.send(response.encode('utf-8'))
                except:
                    pass
                player.request = None
            room.move_ball()
    else:
        print('rooms are empty')
    sleep(0.2)