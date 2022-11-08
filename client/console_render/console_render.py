class ConsoleRender:
    def __init__(self, width, height, left_rocket_x, right_rocket_x):
        self.width = width
        self.height = height
        self.left_rocket_x = left_rocket_x
        self.right_rocket_x = right_rocket_x

    def run(self, ball_x, ball_y, left_rocket_y, right_rocket_y, info_str, score_str):
        main_str = ''
        row = 0
        while row < self.height:
            row_str = ''
            col = 0
            while col < self.width:
                # print info and score
                if row == 0 and col < len(info_str):
                    row_str += info_str[col]
                elif row == 3 and col < len(score_str):
                    row_str += score_str[col]

                # check for left rocket
                elif (row == left_rocket_y or row == (left_rocket_y + 1) or row == (left_rocket_y - 1)) and col == self.left_rocket_x:
                    row_str += '|'

                # check for right rocket
                elif (row == right_rocket_y or row == (right_rocket_y + 1) or row == (right_rocket_y - 1)) and col == self.right_rocket_x:
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