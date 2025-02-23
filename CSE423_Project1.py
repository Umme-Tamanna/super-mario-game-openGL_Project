import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import time
from math import *

# import utility as u
WIDTH = 1000
HEIGHT = 800

# Initial position of mario
polygon_x = 0.0
polygon_y = 0.0

# Movement and jump parameters
move_speed = 0.1
jump_height = 0.2
gravity = 0.1
jumping = False

# Animation
prev_time = time.time()
frame_time = 1.0 / 60.0

# Track Key presses
key_states = {"a": False, "d": False, " ": False}


def addvertex(x, y):
    glVertex2f(x, y)


def color():
    r = random.randint(0, 200) / 255
    g = random.randint(0, 200) / 255
    b = random.randint(0, 200) / 255
    glColor3f(r, g, 0.9)
    # glColor3f(1.0, 1.0, 0.0)


def drawPixel(x, y):
    # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    # glVertex2f(x,y) #jekhane show korbe pixel
    addvertex(x, y)
    glEnd()


def draw8way(x, y, x_c, y_c):
    drawPixel(x_c + x, y_c + y)
    drawPixel(x_c + y, y_c + x)
    drawPixel(x_c - x, y_c + y)
    drawPixel(x_c - y, y_c + x)
    drawPixel(x_c - x, y_c - y)
    drawPixel(x_c - y, y_c - x)
    drawPixel(x_c + x, y_c - y)
    drawPixel(x_c + y, y_c - x)


def drawCircle(r, x_c, y_c):
    x = r
    y = 0
    d = 5 - 4 * r
    color()
    draw8way(x, y, x_c, y_c)

    while y < x:
        if d < 0:
            d += 4 * (2 * y + 3)
            y += 1
        else:
            d += 4 * (2 * y - 2 * x + 5)
            y += 1
            x -= 1
        draw8way(x, y, x_c, y_c)


def iterate():
    glViewport(0, 0, 500, 500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def initialise():
    glClearColor(1, 1, 1, 0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0.0, 100, 0.0, 50)


# ground
def ground():
    glColor3f(0.5, 0.35, 0.05)
    glBegin(GL_POLYGON)
    glVertex2f(0, 0)
    glVertex2f(0, 18)
    glVertex2f(150, 18)
    glVertex2f(150, 0)
    glEnd()


# sky
def sky():
    global score
    glColor3f(0.0, 0.75, 0.9)
    glBegin(GL_POLYGON)
    glVertex2f(0, 19)
    glVertex2f(0, 60)
    glVertex2f(150, 19)
    glVertex2f(150, 60)
    score = 0
    glEnd()


x_value1 = 30
x_value2 = 40
y_value1 = 16
y_value2 = 28

game_over = False

# Obstacles
def obstacles(x_value1, x_value2, y_value1, y_value2):
    check = True
    global x_1, x_2, x_3, x_4, y_1, y_2, y_3, y_4, game_over

    glColor3f(0.0, 0.8, 0.0)
    glBegin(GL_POLYGON)

    glVertex2f(x_value2, y_value2)
    glVertex2f(x_value2, y_value1)
    glVertex2f(x_value1, y_value1)
    glVertex2f(x_value1, y_value2)

    if (x_1 >= x_value1 and x_1 <= x_value2 and y_1 >= y_value1 and y_1 <= y_value2) or (
            x_2 >= x_value1 and x_2 <= x_value2 and y_2 >= y_value1 and y_2 <= y_value2) or \
            (x_3 >= x_value1 and x_3 <= x_value2 and y_3 >= y_value1 and y_3 <= y_value2) or (
            x_4 >= x_value1 and x_4 <= x_value2 and y_4 >= y_value1 and y_4 <= y_value2):
        game_over = True
        print("GAME OVER!")

    glEnd()

def mario():  # Red polygon
    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    glBegin(GL_POLYGON)
    global x_1, x_2, x_3, x_4, y_1, y_2, y_3, y_4

    x_1, y_1 = polygon_x + 5, polygon_y + 15
    x_2, y_2 = polygon_x + 5, polygon_y + 25
    x_3, y_3 = polygon_x + 10, polygon_y + 25
    x_4, y_4 = polygon_x + 10, polygon_y + 15

    glVertex2f(x_3, y_3)
    glVertex2f(x_2, y_2)
    glVertex2f(x_1, y_1)
    glVertex2f(x_4, y_4)
    glEnd()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    ground()
    sky()
    if not game_over:
        mario()
        obstacles(20, 30, 16, 32)
        obstacles(55, 65, 16, 26)
        obstacles(80, 90, 35, 55)

        points(15, 25)  # coin 1
        points(35, 40)  # coin 2
        points(45, 22)  # coin 3
        points(60, 35)  # coin 4
        points(75, 45)  # coin 5
        points(85, 23)  # coin 6

        draw_lines()
        draw_score(score)  # this line to display the score
    # flag()
    else:
        # draw_score(score)
        draw_game_over_text()

    glutSwapBuffers()

def draw_game_over_text():
    glPushMatrix()
    glTranslatef(30, 30, 0)  # Position to display the game over text
    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    glScalef(0.05, 0.05, 0.05)  # Scale down for proper size
    game_over_str = "Game Over"
    for char in game_over_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))

    glPopMatrix()


def keyboard(key, x, y):
    global polygon_x, polygon_y, jumping, key_states

    if key in key_states:
        key_states[key] = True

    if key == b'a':
        key_states["a"] = True
        polygon_x -= move_speed
    if key == b'd':
        key_states["d"] = True
        polygon_x += move_speed

    if key == b' ' and not jumping:
        key_states[" "] = True
        jumping = True


def release_key(key, x, y):
    global key_states
    if key in key_states:
        key_states[key] = False


def update(value):
    global polygon_x, polygon_y, jumping, jump_height, prev_time

    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    prev_time = curr_time

    if jumping:
        target_y = polygon_y + jump_height
        polygon_y = lerp(polygon_y, target_y, elapsed_time * 1000.0)

        if polygon_y >= 0.0:  # Reached or exceeded the jump apex
            jumping = False

    # Gradually decrement polygon_y after jumping
    if not jumping and polygon_y > -1.0:
        polygon_y -= 0.0009  # Adjust the decrement speed as needed

    target_x = polygon_x
    if key_states["a"]:
        target_x -= move_speed
        polygon_x = lerp(polygon_x, target_x, elapsed_time * 1000.0)
        key_states["a"] = False
    if key_states["d"]:
        target_x += move_speed
        polygon_x = lerp(polygon_x, target_x, elapsed_time * 1000.0)
        key_states["d"] = False

    glutPostRedisplay()
    glutTimerFunc(0, update, 0)  # Pass 0 as the value argument


def lerp(a, b, t):
    return a + (b - a) * t


coin_list = []
score = 0


def points(x, y):  # Coins
    global coin_list
    global score
    global position_x, position_y
    global x_1, x_2, x_3, x_4, y_1, y_2, y_3, y_4
    position_x, position_y = x, y
    sides = 30
    radius = 2
    glBegin(GL_POLYGON)
    glColor3f(1, 0.5, 0)

    for i in range(50):  # used to draw coins
        x_value = radius * cos(i * 2 * pi / sides) + position_x
        y_value = radius * sin(i * 2 * pi / sides) + position_y

        glVertex2f(x_value, y_value)  # centre coordinates of coin

        if x_value >= x_1 and y_value >= y_1 and x_value <= x_3 and y_value <= y_3:
            coin_list.append((x_value, y_value))

        if (x_value, y_value) in coin_list:
            glColor3f(0.0, 0.75, 0.9)
            score += 1

        else:
            pass

    glEnd()


#### to show score ############

def draw_score(score):
    glPushMatrix()
    glTranslatef(5, 45, 0)  # Position to display the score
    glColor3f(0.0, 0.0, 0.0)  # black color for text
    glScalef(0.04, 0.04, 0.1)  # Scale down for proper size
    score_str = "Score: " + str(score)
    for char in score_str:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()


def draw_lines():
    glLineWidth(6.5)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 1.0)

    score_str = ""
    score_str += str(score)

    for number in range(len(score_str)):
        a = random.random()
        b = random.random()
        c = random.random()
        glColor3f(a, b, c)

        if score_str[number] == "0":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 110)

            glVertex2f(((number + 1) * 51) - (number * 20), 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)



        elif score_str[number] == "1":

            glVertex2f((number + 1) * 30, 110)
            glVertex2f((number + 1) * 30, 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 29, 180)

            glVertex2f((number + 1) * 29, 110)
            glVertex2f((number + 1) * 31, 110)




        elif score_str[number] == "2":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f(((number + 1) * 51) - (number * 20), 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 150)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f((number + 1) * 30, 150)
            glVertex2f((number + 1) * 30, 110)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

        elif score_str[number] == "3":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 50) - (number * 20), 200)

            glVertex2f(((number + 1) * 50) - (number * 20), 200)
            glVertex2f(((number + 1) * 50) - (number * 20), 150)

            glVertex2f(((number + 1) * 50) - (number * 20), 150)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f(((number + 1) * 50) - (number * 20), 150)
            glVertex2f(((number + 1) * 50) - (number * 20), 110)

            glVertex2f(((number + 1) * 50) - (number * 20), 110)
            glVertex2f((number + 1) * 30, 110)


        elif score_str[number] == "4":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f((number + 1) * 30, 150)
            glVertex2f(((number + 1) * 51) - (number * 20), 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)


        elif score_str[number] == "5":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f(((number + 1) * 51) - (number * 20), 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 150)
            glVertex2f((number + 1) * 30, 150)



        elif score_str[number] == "6":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 110)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f(((number + 1) * 51) - (number * 20), 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 150)
            glVertex2f((number + 1) * 30, 150)

        elif score_str[number] == "7":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f(((number + 1) * 51) - (number * 20), 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)


        elif score_str[number] == "8":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 110)

            glVertex2f(((number + 1) * 51) - (number * 20), 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f((number + 1) * 30, 155)
            glVertex2f(((number + 1) * 51) - (number * 20), 155)


        elif score_str[number] == "9":

            glVertex2f((number + 1) * 30, 200)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

            glVertex2f((number + 1) * 30, 200)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f((number + 1) * 30, 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 110)

            glVertex2f(((number + 1) * 51) - (number * 20), 110)
            glVertex2f(((number + 1) * 51) - (number * 20), 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 150)
            glVertex2f((number + 1) * 30, 150)

            glVertex2f(((number + 1) * 51) - (number * 20), 150)
            glVertex2f(((number + 1) * 51) - (number * 20), 200)

    glEnd()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(900, 900)  # window size
    glutInitWindowPosition(50, 70)
    glutCreateWindow(b"Super Mario Game")  # window name

    # init
    initialise()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(release_key)
    glutTimerFunc(0, update, 0)
    glutMainLoop()


main()
