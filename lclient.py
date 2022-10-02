import socket
from keyboard import is_pressed


def get_parameters(response):
    parameters = response.split(';')
    parameters = [int(param) for param in parameters]
    return parameters


def ball(row, col):
    if row == ball_y and col == ball_x:
        return True
    else:
        return False


def left_rocket(row, col):
    if (row == left_rocket_y or row == (left_rocket_y + 1) or row == (left_rocket_y - 1)) and col == left_rocket_x:
        return True
    else:
        return False


def right_rocket(row, col):
    if (row == right_rocket_y or row == (right_rocket_y + 1) or row == (right_rocket_y - 1)) and col == right_rocket_x:
        return True
    else:
        return False


WIDTH = 120
HEIGHT = 36

lan_ip1 = '192.168.43.201'
lan_ip2 = '192.168.1.107'
local_ip = '127.0.0.1'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((local_ip, 8000))

side = (client_socket.recv(128)).decode('utf-8')
print('my side is', side)
print('wait for second player:')
joined_2_players = (client_socket.recv(128)).decode('utf-8')
print(joined_2_players)

client_socket.send('start parameters'.encode('utf-8'))
parameters = (client_socket.recv(128)).decode('utf-8')
ball_x, ball_y, room_id, game_round, left_player_score, right_player_score = get_parameters(parameters)
left_rocket_x = 2
left_rocket_y = 19
right_rocket_x = 117
right_rocket_y = 19

info_str = f'room id = {room_id};   game_round = {game_round}'
length_info_str = len(info_str)
l_score_str = str(left_player_score)
r_score_str = str(right_player_score)

while True:
    main_str = ''
    row = 0
    while row < HEIGHT:
        row_str = ''
        col = 0
        while col < WIDTH:
            if row == 0 and col < length_info_str:
                row_str += info_str[col]
            elif row == 3 and col == 20:
                row_str += l_score_str
            elif row == 3 and col == 100:
                row_str += r_score_str
            elif left_rocket(row, col):
                row_str += '|'
            elif right_rocket(row, col):
                row_str += '|'
            elif ball(row, col):
                row_str += 'O'
            elif row == 4 or row == 35:
                row_str += '='
            elif (col == 0 or col == 59 or col == 119) and (4 < row < 35):
                row_str += '|'
            else:
                row_str += ' '
            col += 1
        main_str += row_str
        row += 1
    print(main_str)

    if is_pressed('a'):
        client_socket.send('a'.encode('utf-8'))
        response = (client_socket.recv(128)).decode('utf-8')
        left_rocket_y -= 1
        right_rocket_y, ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(response)
    elif is_pressed('z'):
        client_socket.send('z'.encode('utf-8'))
        response = (client_socket.recv(128)).decode('utf-8')
        left_rocket_y += 1
        right_rocket_y, ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(response)
    else:
        client_socket.send('coords right rocket'.encode('utf-8'))
        response = (client_socket.recv(128)).decode('utf-8')
        right_rocket_y, ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(response)

    if ball_x == 0:
        client_socket.send('left is looser'.encode('utf-8'))
        parameters = (client_socket.recv(128)).decode('utf-8')
        ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(parameters)
    info_str = f'room id = {room_id};   game_round = {game_round}'
    length_info_str = len(info_str)
    l_score_str = str(left_player_score)
    r_score_str = str(right_player_score)