import socket
import os
from console_render.console_render import ConsoleRender
from keyboard import is_pressed


# this func for parse response from server
def get_parameters(response):
    parameters = response.split(';')
    parameters = [int(param) for param in parameters]
    return parameters


def left_client():
    global left_rocket_y, right_rocket_y
    render = ConsoleRender(width, height, left_rocket_x, right_rocket_x)
    response = (client_socket.recv(128)).decode('utf-8')
    ball_x, ball_y, room_id, game_round, left_player_score, right_player_score = get_parameters(response)
    info_str = f'room id = {room_id}    game round = {game_round}'
    score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'
    while True:
        render.run(ball_x, ball_y, left_rocket_y, right_rocket_y, info_str, score_str)
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
    global left_rocket_y, right_rocket_y
    render = ConsoleRender(width, height, left_rocket_x, right_rocket_x)
    response = (client_socket.recv(128)).decode('utf-8')
    ball_x, ball_y, room_id, game_round, left_player_score, right_player_score = get_parameters(response)
    info_str = f'room id = {room_id}    game round = {game_round}'
    score_str = f'left player score = {left_player_score}                                             right player score = {right_player_score}'
    while True:
        render.run(ball_x, ball_y, left_rocket_y, right_rocket_y, info_str, score_str)
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


# this width and height of console window in chars
width = 120
height = 36
os.system(f"mode con cols={width} lines={height + 1}")

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
    print('''use keys 'a' and 'z' for move your rocket to up or down''')
    left_client()
else:
    print('''use keys 'k' and 'm' for move your rocket to up or down''')
    right_client()