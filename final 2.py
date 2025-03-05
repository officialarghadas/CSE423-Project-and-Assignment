from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import random

WIDTH, HEIGHT = 600, 500
pointSpeed = 1.5
FREEZE = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.random(), random.random(), random.random())
        self.coordinate_x = random.choice([-1, 1])
        self.coordinate_y = random.choice([-1, 1])
        self.blink = False
        self.blink_time = 0
        self.blink_state = True

    def drawPoints(self):
        if self.blink and not FREEZE:
            if time.time() - self.blink_time > 0.3:
                self.blink_state = not self.blink_state
                self.blink_time = time.time()
            if self.blink_state:
                glColor3fv(self.color)
            else:
                glColor3f(0, 0, 0)
        else:
            glColor3fv(self.color)

        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

    def animate(self):
        if not FREEZE:
            self.x += self.coordinate_x * pointSpeed
            self.y += self.coordinate_y * pointSpeed

            if self.x < -WIDTH // 2 or self.x > WIDTH // 2:
                self.coordinate_x *= -1
            if self.y < -HEIGHT // 2 or self.y > HEIGHT // 2:
                self.coordinate_y *= -1

    def blink_point(self):
        self.blink = True
        self.blink_time = time.time()

points = []

def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.blink_point()
        print("Blinking started")
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        points.append(Point(x - WIDTH // 2, HEIGHT // 2 - y))
        print("Point created")

def keyboard(key, x, y):
    global pointSpeed, FREEZE
    if key == b' ':
        FREEZE = not FREEZE
        print("Freeze!!" if FREEZE else "Unfreeze!!")
    elif key == GLUT_KEY_UP:
        pointSpeed += 0.1
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        pointSpeed -= 0.1
        print("Speed decreased")
        if pointSpeed < 0.1:
            pointSpeed = 0.1

def idle():
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-WIDTH // 2, WIDTH // 2, -HEIGHT // 2, HEIGHT // 2)

    for point in points:
        point.animate()
        point.drawPoints()

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"CSE423 Assignment 1 Part 2")
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboard)
glutIdleFunc(idle)
glutMainLoop()