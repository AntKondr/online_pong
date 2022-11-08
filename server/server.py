import socket
from time import sleep
from room.room import Room


class Player:
    def __init__(self, client_socket, client_adres, side):
        self.socket = client_socket
        self.adres = client_adres
        self.side = side
        self.request = None
        self.score = 0


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