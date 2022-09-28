import socket
from keyboard import is_pressed


def get_coords_rocket_and_ball(response):
    coords = response.split(';')
    coords = [int(coord) for coord in coords]
    return coords


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
HEIGHT = 30

lan_ip1 = '192.168.43.201'
lan_ip2 = '192.168.1.107'
local_ip = '127.0.0.1'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect((lan_ip1, 8000))

while True:
    #client_socket.send('second player'.encode('utf-8'))
    joined_2_players = (client_socket.recv(128)).decode('utf-8')
    print(joined_2_players)
    if joined_2_players == 'True':
        break

client_socket.send('start parameters'.encode('utf-8'))
start_parameters = (client_socket.recv(128)).decode('utf-8')

start_parameters = start_parameters.split(';')
ball_x = int(start_parameters[0])
ball_y = int(start_parameters[1])
direct_ball_x = int(start_parameters[2])
direct_ball_y = int(start_parameters[3])
left_rocket_x = 2
left_rocket_y = 14
right_rocket_x = 117
right_rocket_y = 14

while True:
    main_str = ''
    row = 0
    while row < HEIGHT:
        row_str = ''
        col = 0
        while col < WIDTH:
            if left_rocket(row, col):
                row_str += '|'
            elif right_rocket(row, col):
                row_str += '|'
            elif ball(row, col):
                row_str += 'O'
            elif row == 0 or row == 29:
                row_str += '='
            elif col == 0 or col == 59 or col == 119:
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
        right_rocket_y, ball_x, ball_y = get_coords_rocket_and_ball(response)
    elif is_pressed('z'):
        client_socket.send('z'.encode('utf-8'))
        response = (client_socket.recv(128)).decode('utf-8')
        left_rocket_y += 1
        right_rocket_y, ball_x, ball_y = get_coords_rocket_and_ball(response)
    else:
        client_socket.send('coords right rocket'.encode('utf-8'))
        response = (client_socket.recv(128)).decode('utf-8')
        right_rocket_y, ball_x, ball_y = get_coords_rocket_and_ball(response)

    if ball_x == 0:
        client_socket.send('left is looser'.encode('utf-8'))
        print(' '*51 + 'RIGHT PLAYER WIN!!!')
        break
    elif ball_x == 119:
        client_socket.send('right is looser'.encode('utf-8'))
        print(' '*51 + 'LEFT PLAYER WIN!!!')
        break