from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


################################################


theme = "light"
rain_x = rain_y = 0
speed = 0.2    ## rain speed
rain_direction = 0


#################################################


def draw_main_house():
   background_color()
   glBegin(GL_LINES)
   glVertex2f(400, 100)
   glVertex2f(800, 100)
   glVertex2f(400, 300)
   glVertex2f(800, 300)
   glVertex2f(400, 100)
   glVertex2f(400, 300)
   glVertex2f(800, 100)
   glVertex2f(800, 300)
   glEnd()


def draw_door():
   glBegin(GL_LINES)
   glVertex2f(570, 100)
   glVertex2f(570, 201)
   glVertex2f(630, 100)
   glVertex2f(630, 200)
   glVertex2f(570, 200)
   glVertex2f(630, 200)
   glEnd()


def draw_roof():
   background_color()
   glBegin(GL_TRIANGLES)
   glVertex2f(380, 300)
   glVertex2f(820, 300)
   glVertex2f(600, 520)
   glEnd()




############################################


def draw_short_line(x, y):
   global rain_direction


   if rain_direction == 0:
       glBegin(GL_LINES)
       glVertex2f(x + 0, y + 0)
       glVertex2f(x + 0, y + 15)
       glEnd()


   elif rain_direction == 1:
       glBegin(GL_LINES)
       glVertex2f(x + 0, y + 0)
       glVertex2f(x + 8, y + 8)
       glEnd()


   elif rain_direction == 2:
       glBegin(GL_LINES)
       glVertex2f(x + 0, y + 0)
       glVertex2f(x - 8, y + 8)
       glEnd()


#######################################################


def background_color():
   global theme


   if theme == "light":
       glClearColor(0, 0, 0, 0)
       glColor3f(1.0, 1.0, 1.0)


   else:
       glClearColor(1, 1, 1, 1)
       glColor3f(0, 0, 0)


#######################################################




def specialKeyListener1(key, x, y):
   global rain_direction, speed, theme


   if key == GLUT_KEY_UP:
       theme = "light"
       rain_direction = 0
   if key == GLUT_KEY_DOWN:
       theme = "dark"
       rain_direction = 0
   if key == GLUT_KEY_LEFT:
       rain_direction = 1
       speed = 0.2
   if key == GLUT_KEY_RIGHT:
       rain_direction = 2
       speed = 0.2


##########################################


def animate():
   glutPostRedisplay()


   global rain_x, rain_y, speed, rain_direction


   if rain_direction == 0:
       rain_y = (rain_y - speed) % 20


   elif rain_direction == 1:
       rain_y = (rain_y - speed) % 20
       rain_x = (rain_x - speed) % 20


   elif rain_direction == 2:
       rain_y = (rain_y - speed) % 20
       rain_x = (rain_x + speed) % 20


###############################################


def rain():
   global rain_y, rain_x


   i = 100  # x start


   while i < 1000:  # x end
       if i % 20 == 0:
           j = 520   # y start -- roof er upor
           while j > 320:   # y end -- roof er niche
               draw_short_line(i + 10 + rain_x, j + rain_y)
               j -= 20
       else:
           j = 530  # y start -- roof er upor
           while j > 320:  # y end -- roof er niche
               draw_short_line(i + 10 + rain_x, j + rain_y)
               j -= 20


       i += 10


#############################################################


def iterate():
   glViewport(0, 0, 1000, 1000)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()


###################################################################


def showscreen():
   glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
   glLoadIdentity()
   iterate()
   background_color()
   draw_roof()
   draw_main_house()
   draw_door()
   rain()


   glutSwapBuffers()


##############################################################


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1100, 800)
glutInitWindowPosition(0, 0)


wind = glutCreateWindow(b"House in a rainy day")
glutDisplayFunc(showscreen)
glutSpecialFunc(specialKeyListener1)
glutIdleFunc(animate)
glutMainLoop()

