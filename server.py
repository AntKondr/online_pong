import socket
from random import randint
from time import sleep


class Player:
    def __init__(self, client_socket, client_adres, side):
        self.socket = client_socket
        self.adres = client_adres
        self.side = side
        self.request = None
        self.score = 0


class Room:
    sides = ('l', 'r')
    directs = (-1, 1)
    left_rocket_x = 2
    right_rocket_x = 117

    def __init__(self, pair_players, room_id):
        self.pair_players = pair_players
        self.left_player = pair_players[0]
        self.right_player = pair_players[1]
        self.id = room_id
        self.game_round = 1
        self.left_rocket_y = 19
        self.right_rocket_y = 19
        self.delay = 0

    def set_start_parameters(self):
        serving_side = Room.sides[randint(0, 1)]
        if serving_side == 'l':
            self.ball_x, self.ball_y = (3, self.left_rocket_y)
            self.direct_ball_x = Room.directs[1]
        else:
            self.ball_x, self.ball_y = (116, self.right_rocket_y)
            self.direct_ball_x = Room.directs[0]
        self.direct_ball_y = Room.directs[randint(0, 1)]

    def get_start_parameters(self):
        return f'{self.ball_x};{self.ball_y};{self.id};{self.game_round};{self.left_player.score};{self.right_player.score}'

    def move_ball(self):
        if self.ball_x == (Room.right_rocket_x - 1) and ((self.ball_y == self.right_rocket_y) or (self.ball_y == self.right_rocket_y + 1) or (self.ball_y == self.right_rocket_y - 1)):
            self.direct_ball_x = -1
        elif self.ball_x == (Room.left_rocket_x + 1) and ((self.ball_y == self.left_rocket_y) or (self.ball_y == self.left_rocket_y + 1) or (self.ball_y == self.left_rocket_y - 1)):
            self.direct_ball_x = 1

        if self.ball_y == 34:
            self.direct_ball_y = -1
        elif self.ball_y == 5:
            self.direct_ball_y = 1

        self.ball_x += self.direct_ball_x
        self.ball_y += self.direct_ball_y

        if self.ball_x == 0:
            self.right_player.score += 1
            self.game_round += 1
            self.set_start_parameters()
        elif self.ball_x == 119:
            self.left_player.score += 1
            self.game_round += 1
            self.set_start_parameters()

    def __get_parameters(self, side):
        if side == 'l':
            return f'{self.right_rocket_y};{self.ball_x};{self.ball_y};{self.game_round};{self.left_player.score};{self.right_player.score}'
        else:
            return f'{self.left_rocket_y};{self.ball_x};{self.ball_y};{self.game_round};{self.left_player.score};{self.right_player.score}'

    def form_response(self, request):
        if request == 'a':
            self.left_rocket_y -= 1
            return self.__get_parameters('l')
        elif request == 'z':
            self.left_rocket_y += 1
            return self.__get_parameters('l')

        elif request == 'k':
            self.right_rocket_y -= 1
            return self.__get_parameters('r')
        elif request == 'm':
            self.right_rocket_y += 1
            return self.__get_parameters('r')

        elif request == 'coords left rocket':
            return self.__get_parameters('r')

        elif request == 'coords right rocket':
            return self.__get_parameters('l')


ALLOWED_IP = ['127.0.0.1', '192.168.43.201', '192.168.1.107']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server_socket.bind((ALLOWED_IP[0], 8000))
server_socket.setblocking(False)
server_socket.listen()
print('server online ping-pong started\n')

room_id = 1
rooms = []
pair_players = []
run = True
tick = 1
while run:
    try:
        client_socket, client_adres = server_socket.accept()
        client_socket.setblocking(False)
        if len(pair_players) == 0:
            side = 'left'
        else:
            side = 'right'
        new_player = Player(client_socket, client_adres, side)
        print('connect', new_player.adres)
        new_player.socket.send((new_player.side).encode('utf-8'))
        pair_players.append(new_player)
    except BlockingIOError:
        pass

    if len(pair_players) == 2:
        new_room = Room(pair_players, room_id)
        new_room.set_start_parameters()
        rooms.append(new_room)
        room_id += 1
        pair_players = []
        for player in new_room.pair_players:
            player.socket.send(new_room.get_start_parameters().encode('utf-8'))

    for room in rooms:
        if room.delay >= 10:
            print('in room', room.id)
            for player in room.pair_players:
                try:
                    player.request = player.socket.recv(128).decode('utf-8')
                    print('request =>', player.request)
                except BlockingIOError:
                    print('запроса от игрока', player.adres, 'не удалось')
                try:
                    response = room.form_response(player.request)
                    player.socket.send(response.encode('utf-8'))
                except AttributeError:
                    print('ответ игроку', player.adres, 'не удалось\n')
            room.move_ball()
        else:
            room.delay += 1
    tick += 1
    sleep(0.1)