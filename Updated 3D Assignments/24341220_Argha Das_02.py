from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import sys
import os

# Window size
window_width = 800
window_height = 600

# Game variables
game_state = "playing"  # playing, paused, gameover
score = 0
should_exit = False  # Flag for safe exit

# Diamond properties
diamond_x = random.randint(50, window_width - 50)
diamond_y = window_height - 20
diamond_size = 25
diamond_speed = 90.0  # pixels per second
diamond_color = (1.0, 0.5, 0.8)

# Catcher properties
catcher_x = window_width // 2 - 40
catcher_y = 20
catcher_width = 100
catched_bottom_width = 60
catcher_height = 30
catcher_color = (1.0, 1.0, .0)

# Button properties
restart_btn_x = 20
restart_btn_y = window_height - 40
restart_btn_width = 40
restart_btn_height = 35

pause_btn_x = window_width // 2 - 25
pause_btn_y = window_height - 40
pause_btn_width = 50
pause_btn_height = 35

exit_btn_x = window_width - 60
exit_btn_y = window_height - 40
exit_btn_width = 40
exit_btn_height = 35

# Time tracking
last_time = time.time()


def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx >= 0 and dy < 0
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  # dx >= 0 and dy < 0
            return 6

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    
    # Convert to zone 0
    x1_z0, y1_z0 = convert_to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = convert_to_zone0(x2, y2, zone)
    
    
    if x1_z0 > x2_z0:
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0
    
    # Draw using midpoint algorithm
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    
    x = x1_z0
    y = y1_z0
    
    glBegin(GL_POINTS)
    
    # First point
    orig_x, orig_y = convert_from_zone0(x, y, zone)
    glVertex2i(orig_x, orig_y)
    
    # Remaining points
    while x < x2_z0:
        if d > 0:  # Choose NE
            d += incNE
            x += 1
            y += 1
        else:  # Choose E
            d += incE
            x += 1
        
        orig_x, orig_y = convert_from_zone0(x, y, zone)
        glVertex2i(orig_x, orig_y)
    
    glEnd()


def draw_shape(points):
    for i in range(len(points)):
        draw_line(*points[i], *points[(i+1) % len(points)])


def draw_diamond(x, y, size):
    points = [
        (x, y + size),     # Top
        (x + size, y),     # Right
        (x, y - size),     # Bottom
        (x - size, y)      # Left
    ]
    draw_shape(points)

def draw_catcher(x, y, width, bottom_width, height):
    cx = x + width // 2
    points = [
        (cx - bottom_width//2, y),
        (cx + bottom_width//2, y),
        (cx + width//2, y + height),
        (cx - width//2, y + height)
    ]
    draw_shape(points)

def draw_restart_button(x, y, width, height):
    mid_y = y + height // 2
    points = [
        (x + width - 5, y + 5),
        (x + 5, mid_y),
        (x + width - 5, y + height - 5)
    ]
    draw_shape(points)

def draw_play_pause_button(x, y, width, height, is_playing):
    if is_playing:
        bar_width = width // 5
        gap = width // 4
        for i in [0, 1]:
            px = x + gap + i * (bar_width + gap)
            draw_shape([
                (px, y + 5), (px + bar_width, y + 5),
                (px + bar_width, y + height - 5), (px, y + height - 5)
            ])
    else:
        points = [(x + 10, y + 5), (x + 10, y + height - 5), (x + width - 10, y + height // 2)]
        draw_shape(points)

def draw_exit_button(x, y, width, height):
    draw_line(x + 10, y + 10, x + width - 10, y + height - 10)
    draw_line(x + 10, y + height - 10, x + width - 10, y + 10)

# Game logic
def check_collision():
    return (
        diamond_x - diamond_size < catcher_x + catcher_width and
        diamond_x + diamond_size > catcher_x and
        diamond_y - diamond_size < catcher_y + catcher_height and
        diamond_y + diamond_size > catcher_y
    )

def exit_game():
    print("Goodbye!  Score:", score)
    glutDestroyWindow(window)
    os._exit(0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(*diamond_color)
    draw_diamond(int(diamond_x), int(diamond_y), diamond_size)

    glColor3f(*catcher_color)
    draw_catcher(catcher_x, catcher_y, catcher_width, catched_bottom_width, catcher_height)

    glColor3f(0.0, 0.8, 0.8)
    draw_restart_button(restart_btn_x, restart_btn_y, restart_btn_width, restart_btn_height)

    glColor3f(1.0, 0.75, 0.0)
    draw_play_pause_button(pause_btn_x, pause_btn_y, pause_btn_width, pause_btn_height, game_state == "playing")

    glColor3f(1.0, 0.0, 0.0)
    draw_exit_button(exit_btn_x, exit_btn_y, exit_btn_width, exit_btn_height)

    glutSwapBuffers()

def update(value):
    global diamond_x, diamond_y, diamond_speed, diamond_color
    global catcher_x, catcher_color, game_state, score, last_time, should_exit

    if should_exit:
        exit_game()

    now = time.time()
    dt = now - last_time
    last_time = now

    if game_state == "playing":
        diamond_y -= diamond_speed * dt
        diamond_speed += 5 * dt

        if check_collision():
            score += 1
            print("Score:", score)
            diamond_x = random.randint(50, window_width - 50)
            diamond_y = window_height - 20
            diamond_speed = 90.0 + score * 5
            diamond_color = (random.random(), random.random(), random.random())
        elif diamond_y < 0:
            game_state = "gameover"
            catcher_color = (1.0, 0.0, 0.0)
            print("Game Over!  Score:", score)

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global should_exit
    if key in [b'\x1b', b'q', b'Q']:
        should_exit = True

def special_keys(key, x, y):
    global catcher_x
    if game_state == "playing":
        if key == GLUT_KEY_LEFT:
            catcher_x = max(0, catcher_x - 20)
        elif key == GLUT_KEY_RIGHT:
            catcher_x = min(window_width - catcher_width, catcher_x + 20)
    glutPostRedisplay()

def mouse(button, state, x, y):
    global game_state, diamond_x, diamond_y, diamond_speed, diamond_color
    global catcher_x, catcher_color, score, should_exit

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mouse_y = window_height - y
        if restart_btn_x <= x <= restart_btn_x + restart_btn_width and restart_btn_y <= mouse_y <= restart_btn_y + restart_btn_height:
            game_state = "playing"
            score = 0
            diamond_x = random.randint(50, window_width - 50)
            diamond_y = window_height - 20
            diamond_speed = 90.0
            diamond_color = (random.random(), random.random(), random.random())
            catcher_x = window_width // 2 - 50
            catcher_color = (1.0, 1.0, 1.0)
            print("Starting Over")
        elif pause_btn_x <= x <= pause_btn_x + pause_btn_width and pause_btn_y <= mouse_y <= pause_btn_y + pause_btn_height:
            if game_state == "playing":
                game_state = "paused"
                print("Game Paused")
            elif game_state == "paused":
                game_state = "playing"
                print("Game Resumed")
        elif exit_btn_x <= x <= exit_btn_x + exit_btn_width and exit_btn_y <= mouse_y <= exit_btn_y + exit_btn_height:
            should_exit = True

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glPointSize(2)

def main():
    global window
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    window = glutCreateWindow(b"Catch the Diamonds!")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutTimerFunc(16, update, 0)
    print("catch the diamonds!")
    glutMainLoop()

if __name__ == "__main__":
    main()
