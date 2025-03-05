from OpenGL.GL import *
from OpenGL.GLUT import *
import random

#######################################################

W_Width, W_Height = 500, 800

bullet = []
circle_radius = 15
unique_circle_radius = 20
score = 0
misfires = 0
freeze = False
gameover = 0

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



class Catcher:
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


def midpointcircle(radius, centerX=0, centerY=0):
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

bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
bubble.sort(key=lambda b: b.x)
catcher = Catcher()

###################################################################
def draw_bullet():
    global bullet
    glPointSize(2)
    glColor3f(1, 1, 1)
    for i in bullet:
        midpointcircle(8, i[0], i[1])

####################################################################
# def draw_bubble():
#     global bubble
#     glPointSize(2)
#
#     for b in bubble:
#         glColor3f(b.color[0], b.color[1], b.color[2])
#         midpointcircle(b.r, b.x, b.y)
def draw_bubble():
    global bubble
    glPointSize(2)

    for i in range(len(bubble)):
        if bubble[i].special:  # Draw special bubble
            bubble[i].update_radius()
            glColor3f(1, 0, 0)  # Red for special bubbles
        else:  # Normal bubbles
            glColor3f(bubble[i].color[0], bubble[i].color[1], bubble[i].color[2])

        # Conditions to draw the bubble (no overlaps, within range)
        if i == 0 or (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
            midpointcircle(bubble[i].r, bubble[i].x, bubble[i].y)

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
    global catcher

    # shooter
    draw_spaceship(centerX=catcher.x, centerY=-365)

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
    if freeze:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

#####################################################################
def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

#######################################################################
def keyboardListener(key, x, y):
    global bullet, freeze, gameover, catcher
    if key == b' ':
        if not freeze and gameover < 3:
            bullet.append([catcher.x, -365])
    elif key == b'a':
        if catcher.x > -230 and not freeze:
            catcher.x -= 10
    elif key == b'd':
        if catcher.x < 230 and not freeze:
            catcher.x += 10
    glutPostRedisplay()




#########################################################################

def mouseListener(button, state, x, y):
    global freeze, gameover, catcher, score, bubble, bullet, misfires
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
    #     c_x, c_y = convert_coordinate(x, y)
    #     # print(c_x, c_y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            freeze = False
            print('Starting Over')
            bubble = [Bubble(), Bubble(), Bubble(), Bubble(), Bubble()]
            bubble.sort(key=lambda b: b.x)
            score = 0
            gameover = 0
            misfires = 0
            bullet = []

        if 170 < c_x < 216 and 330 < c_y < 370:
            print('Goodbye! Score:', score)
            glutLeaveMainLoop()

        if -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze

    # if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
    #     pass

    glutPostRedisplay()

#############################################################

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullet()
    draw_bubble()
    glutSwapBuffers()
################################################################################
import time
def animate():
    current_time = time.time()
    delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    animate.start_time = current_time

    global freeze, bubble, catcher, gameover, score, bullet, misfires
    if not freeze and gameover < 3 and misfires < 3:
        delidx = []
        for i in range(len(bullet)):
            if bullet[i][1] < 400:
                bullet[i][1] += 10
            else:
                delidx.append(i)
                misfires += 1
        try:
            for j in delidx:
                del bullet[j]
        except:
            pass

        for i in range(len(bubble)):
            if i == 0:
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
                    bubble.sort(key=lambda b: b.y)
            elif (bubble[i - 1].y < (330 - 2 * bubble[i].r - 2 * bubble[i - 1].r)) or (
                    abs(bubble[i - 1].x - bubble[i].x) > (2 * bubble[i - 1].r + 2 * bubble[i].r + 10)):
                if bubble[i].y > -400:
                    bubble[i].y -= (10 + score * 5) * delta_time
                else:
                    gameover += 1
                    del bubble[i]
                    bubble.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
                    bubble.sort(key=lambda b: b.y)
        try:
            for i in range(len(bubble)):
                # Collision with the spaceship
                if abs(bubble[i].y - -345) < (bubble[i].r) and abs(bubble[i].x - catcher.x) < (bubble[i].r + 20):
                    gameover += 3  # game over
                for j in range(len(bullet)):
                    if abs(bubble[i].y - bullet[j][1]) < (bubble[i].r + 15) and abs(bubble[i].x - bullet[j][0]) < (
                            bubble[i].r + 20):
                        if bubble[i].special:
                            score += 5  # Special bubbles give more points
                        else:
                            score += 1
                        print("Score:", score)
                        del bubble[i]
                        del bullet[j]
                        bubble.append(Bubble(special=random.random() < 0.2))  # 20% chance for special bubble
        except:
            pass

    # Game over condition
    if (gameover >= 3 or misfires >= 3) and not freeze:
        print("Game Over! Score:", score)
        freeze = True
        bubble = []  # Clear bubbles

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
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Shoot The Circles!")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()