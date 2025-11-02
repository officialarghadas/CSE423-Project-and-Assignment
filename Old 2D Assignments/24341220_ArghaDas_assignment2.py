from OpenGL.GL import *
from OpenGL.GLUT import *
import random

#######################################################

window_width, window_height = 500, 800

bullets = []
default_circle_radius = 15
special_circle_radius = 20
score = 0
misfires = 0
is_paused = False
game_over_count = 0

###################################################################
class Bubble:
    def __init__(self, special=False):
        self.x = random.randint(-220, 220)
        self.y = 330
        self.r = random.randint(20, 25)
        self.color = [random.uniform(0.3, 1.0) for _ in range(3)]
        self.special = special
        self.r_delta = 0.5  # Used for radius animation in special bubbles

    def update_radius(self):
        """Expand and shrink the radius if it's a special bubble."""
        if self.special:
            self.r += self.r_delta
            if self.r > 30 or self.r < 15:  # Bounds for radius expansion/shrink
                self.r_delta *= -1


class Spaceship:
    def __init__(self):
        self.x = 0
        self.color = [1, 1, 1]

###################################### Mid-Point Line Drawing Algorithm
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)


def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)

    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)


########### Mid-Point Circle Drawing Algorithm

def midpoint_circle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

##################################################################

bubbles = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubbles.sort(key=lambda b: b.x)
spaceship = Spaceship()

###################################################################
def draw_bullets():
    global bullets
    glPointSize(2)
    glColor3f(1, 1, 1)
    for bullet in bullets:
        midpoint_circle(8, bullet[0], bullet[1])

####################################################################
def draw_bubbles():
    global bubbles
    glPointSize(2)

    for i in range(len(bubbles)):
        if bubbles[i].special:  # Draw special bubble
            bubbles[i].update_radius()
            glColor3f(1, 0, 0)  # Red for special bubbles
        else:  # Normal bubbles
            glColor3f(bubbles[i].color[0], bubbles[i].color[1], bubbles[i].color[2])

        if i == 0 or (bubbles[i - 1].y < (330 - 2 * bubbles[i].r - 2 * bubbles[i - 1].r)) or (
                abs(bubbles[i - 1].x - bubbles[i].x) > (2 * bubbles[i - 1].r + 2 * bubbles[i].r + 10)):
            midpoint_circle(bubbles[i].r, bubbles[i].x, bubbles[i].y)

def draw_spaceship(centerX=0, centerY=-365):
    # Rocket body (rectangle)
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0)  
    glVertex2f(centerX - 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY - 20) 
    glVertex2f(centerX - 10, centerY - 20)  
    glEnd()
    
    # Rocket nose (triangle)
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 1) 
    glVertex2f(centerX, centerY + 100)  
    glVertex2f(centerX - 10, centerY + 80)  
    glVertex2f(centerX + 10, centerY + 80)  
    glEnd()
    
    # Left fin
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0.5) 
    glVertex2f(centerX - 10, centerY - 20) 
    glVertex2f(centerX - 30, centerY - 40) 
    glVertex2f(centerX - 10, centerY - 40)  
    glEnd()
    
    # Right fin
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0.5, 0.5) 
    glVertex2f(centerX + 10, centerY - 20) 
    glVertex2f(centerX + 30, centerY - 40) 
    glVertex2f(centerX + 10, centerY - 40)  
    glEnd()
    
    # Rocket thrusters
    for i in range(3):
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 0.5, 0)  
        x_offset = (i - 1) * 10  
        glVertex2f(centerX - 5 + x_offset, centerY - 40)  
        glVertex2f(centerX + 5 + x_offset, centerY - 40)  
        glVertex2f(centerX + 5 + x_offset, centerY - 60)  
        glVertex2f(centerX - 5 + x_offset, centerY - 60) 
        glEnd()

###############################################################################
def draw_ui():
    global spaceship

    # shooter
    draw_spaceship(centerX=spaceship.x, centerY=-365)

    # Left button
    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    # Right Cross Button
    glPointSize(4)
    glColor3f(0.9, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    # Middle Pause Button
    glPointSize(4)
    glColor3f(1, .5, 0)
    if is_paused:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

#####################################################################
def convert_coordinate(x, y):
    global window_width, window_height
    a = x - (window_width / 2)
    b = (window_height / 2) - y
    return a, b

#######################################################################
def keyboard_listener(key, x, y):
    global bullets, is_paused, game_over_count, spaceship
    if key == b' ':
        if not is_paused and game_over_count < 3:
            bullets.append([spaceship.x, -365])
    elif key == b'a':
        if spaceship.x > -230 and not is_paused:
            spaceship.x -= 10
    elif key == b'd':
        if spaceship.x < 230 and not is_paused:
            spaceship.x += 10
    glutPostRedisplay()

#########################################################################

def mouse_listener(button, state, x, y):
    global is_paused, game_over_count, spaceship, score, bubbles, bullets, misfires
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            is_paused = False
            print('Starting Over')
            bubbles = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubbles.sort(key=lambda b: b.x)
            score = 0
            game_over_count = 0
            misfires = 0
            bullets = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            is_paused = not is_paused

    glutPostRedisplay()

#############################################################

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullets()
    draw_bubbles()
    glutSwapBuffers()
################################################################################
import time
def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global is_paused, bubbles, spaceship, game_over_count, score, bullets, misfires
    if not is_paused and game_over_count < 3 and misfires < 3:
        delidx = []
        for i in range(len(bullets)):
            if bullets[i][1] < 400:
                bullets[i][1] += 10
            else:
                delidx.append(i)
                misfires += 1
        try:
            for j in delidx:
                del bullets[j]
        except:
            pass

        for i in range(len(bubbles)):
            if i == 0:
                if bubbles[i].y > -400:
                    bubbles[i].y -= (10 + score * 5) * delta_time
                else:
                    game_over_count += 1
                    del bubbles[i]
                    bubbles.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
                    bubbles.sort(key=lambda b: b.y)
            elif (bubbles[i - 1].y < (330 - 2 * bubbles[i].r - 2 * bubbles[i - 1].r)) or (
                    abs(bubbles[i - 1].x - bubbles[i].x) > (2 * bubbles[i - 1].r + 2 * bubbles[i].r + 10)):
                if bubbles[i].y > -400:
                    bubbles[i].y -= (10 + score * 5) * delta_time
                else:
                    game_over_count += 1
                    del bubbles[i]
                    bubbles.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
                    bubbles.sort(key=lambda b: b.y)
        try:
            for i in range(len(bubbles)):
                if abs(bubbles[i].y - -345) < (bubbles[i].r) and abs(bubbles[i].x - spaceship.x) < (bubbles[i].r + 20):
                    game_over_count += 3  # game over
                for j in range(len(bullets)):
                    if abs(bubbles[i].y - bullets[j][1]) < (bubbles[i].r + 15) and abs(bubbles[i].x - bullets[j][0]) < (
                            bubbles[i].r + 20):
                        if bubbles[i].special:
                            score += 5  # Special bubbles give more points
                        else:
                            score += 1
                        print("Score:", score)
                        del bubbles[i]
                        del bullets[j]
                        bubbles.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
        except:
            pass

    if (game_over_count >= 3 or misfires >= 3) and not is_paused:
        print("Game Over! Score:", score)
        is_paused = True
        bubbles = []  # Clear bubbles

    time.sleep(1 / 1000)
    glutPostRedisplay()

################################################################################

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)

###############################################################

glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Shoot The Circles!")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboard_listener)
glutMouseFunc(mouse_listener)

glutMainLoop()
