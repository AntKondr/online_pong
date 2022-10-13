import socket
from keyboard import is_pressed


# this func for parse response from server
def get_parameters(response):
    parameters = response.split(';')
    parameters = [int(param) for param in parameters]
    return parameters


# this width and height of console window in chars
width = 120
height = 36


# this func for print a game process in console window
def render():
    main_str = ''
    row = 0
    while row < height:
        row_str = ''
        col = 0
        while col < width:
            # print info and score
            if row == 0 and col < len(info_str):
                row_str += info_str[col]
            elif row == 3 and col < len(score_str):
                row_str += score_str[col]

            # check for left rocket
            elif (row == left_rocket_y or row == (left_rocket_y + 1) or row == (left_rocket_y - 1)) and col == left_rocket_x:
                row_str += '|'

            # check for right rocket
            elif (row == right_rocket_y or row == (right_rocket_y + 1) or row == (right_rocket_y - 1)) and col == right_rocket_x:
                row_str += '|'

            # check for ball
            elif row == ball_y and col == ball_x:
                row_str += 'O'

            # check for edges and void
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


def left_client():
    global ball_x, ball_y, left_rocket_y, right_rocket_y, info_str, score_str
    response = (client_socket.recv(128)).decode('utf-8')
    ball_x, ball_y, room_id, game_round, left_player_score, right_player_score = get_parameters(response)
    info_str = f'room id = {room_id}    game round = {game_round}'
    score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'
    while True:
        render()
        if is_pressed('a'):
            client_socket.send('a'.encode('utf-8'))
            left_rocket_y -= 1
        elif is_pressed('z'):
            client_socket.send('z'.encode('utf-8'))
            left_rocket_y += 1
        else:
            client_socket.send('coords right rocket'.encode('utf-8'))

        response = (client_socket.recv(128)).decode('utf-8')
        right_rocket_y, ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(response)
        info_str = f'room id = {room_id}    game round = {game_round}'
        score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'


def right_client():
    global ball_x, ball_y, left_rocket_y, right_rocket_y, info_str, score_str
    response = (client_socket.recv(128)).decode('utf-8')
    ball_x, ball_y, room_id, game_round, left_player_score, right_player_score = get_parameters(response)
    info_str = f'room id = {room_id}    game round = {game_round}'
    score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'
    while True:
        render()
        if is_pressed('k'):
            client_socket.send('k'.encode('utf-8'))
            right_rocket_y -= 1
        elif is_pressed('m'):
            client_socket.send('m'.encode('utf-8'))
            right_rocket_y += 1
        else:
            client_socket.send('coords left rocket'.encode('utf-8'))

        response = (client_socket.recv(128)).decode('utf-8')
        left_rocket_y, ball_x, ball_y, game_round, left_player_score, right_player_score = get_parameters(response)
        info_str = f'room id = {room_id}    game round = {game_round}'
        score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'


left_rocket_x = 2
right_rocket_x = 117
left_rocket_y = 19
right_rocket_y = 19

ALLOWED_IP = ['127.0.0.1', '192.168.43.201', '192.168.1.107']

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((ALLOWED_IP[0], 8000))

side = (client_socket.recv(128)).decode('utf-8')
print('your side:', side, '\nwait for second player....')

if side == 'left':
    left_client()
else:
    right_client()