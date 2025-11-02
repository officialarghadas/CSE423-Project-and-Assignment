from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import ctypes

#GLUT_BITMAP_HELVETICA_18 = ctypes.c_void_p(0x0004)
GLUT_BITMAP_TIMES_ROMAN_24 = ctypes.c_void_p(0x0008)

grid_size = 15
cell_size = 1.0

camera_angle = 0
camera_radius = 15
camera_height = 18
camera_mode= "3rd"

player_x = grid_size / 2
player_z = grid_size / 2
player_angle = 0
pink = (1.0, 0.8, 0.9)
green = (0.8, 1.0, 0.8)
cheat_mode = False
cooldown = 0
cheat_index = 0
score = 0
lives = 5
missed_bullets = 0
game_over = False

enemies= []
num_enemies = 5
bullets = []
bullet_speed = 0.3

#All shapes drawings
def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            color = pink if (i + j) % 2 == 0 else green
            glColor3f(*color)
            glBegin(GL_QUADS)
            glVertex3f(i * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, j * cell_size)
            glVertex3f((i + 1) * cell_size, 0, (j + 1) * cell_size)
            glVertex3f(i * cell_size, 0, (j + 1) * cell_size)
            glEnd()

def draw_walls():
    height = 1
    thickness = 0.2
    length = grid_size * cell_size

    # Bottom wall=blue
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(length / 2, height / 2, thickness / 2)
    glScalef(length, height, thickness)
    glutSolidCube(1)
    glPopMatrix()

    # Top wall=green
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(length / 2, height / 2, length - thickness / 2)
    glScalef(length, height, thickness)
    glutSolidCube(1)
    glPopMatrix()

    # Left wall=cyan
    glColor3f(0.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(thickness / 2, height / 2, length / 2)
    glScalef(thickness, height, length)
    glutSolidCube(1)
    glPopMatrix()

    # Right wall=magenta
    glColor3f(1.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(length - thickness / 2, height / 2, length / 2)
    glScalef(thickness, height, length)
    glutSolidCube(1)
    glPopMatrix()


def draw_player():
    glPushMatrix()
    glTranslatef(player_x, 0, player_z)
    glRotatef(player_angle, 0, 1, 0)
    glScalef(0.9, 0.9, 0.9)

    if game_over:
        glRotatef(90, 1, 0, 0)
#legs
    glColor3f(0.0, 0.0, 1.0)
    for x_offset in [-0.2, 0.2]:
        glPushMatrix()
        glTranslatef(x_offset, 0.4, 0)
        glRotatef(-90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.1, 0.05, 0.4, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()
#body
    glColor3f(0.8, 0.4, 0.0)
    glPushMatrix()
    glTranslatef(0, 1.0, 0)
    glScalef(0.4, 0.6, 0.2)
    glutSolidCube(1)
    glPopMatrix()
#arms
    glColor3f(0.96, 0.8, 0.69)
    for x_offset in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(x_offset, 1.2, 0.1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.1, 0.05, 0.4, 20, 20)
        gluDeleteQuadric(quad)
        glPopMatrix()
#gun
    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()
    glTranslatef(0, 1.2, 0.1)
    quad = gluNewQuadric()
    gluCylinder(quad, 0.08, 0.0, 0.8, 20, 20)
    gluDeleteQuadric(quad)
    glPopMatrix()
#head
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 1.65, 0)
    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()

    glPopMatrix()

def draw_bullets():
    glColor3f(0.8, 0.33, 0.0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['x'], 1.2, bullet['z'])
        glScalef(0.15, 0.15, 0.15)
        glutSolidCube(1)
        glPopMatrix()

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy['x'], 0.4, enemy['z'])
        glScalef(enemy['scale'], enemy['scale'], enemy['scale'])
#head
        glColor3f(1.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, 0.2, 0)
        glutSolidSphere(0.2, 20, 20)
        glPopMatrix()
#body
        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(0, 0.45, 0)
        glutSolidSphere(0.12, 20, 20)
        glPopMatrix()

        glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def update_bullets():
    global bullets, missed_bullets, score

    new_bullets = []

    if cheat_mode:
        fcheat_mode()

    for bullet in bullets:
        rad = math.radians(bullet['angle'])
        bullet['x'] += bullet_speed * math.sin(rad)
        bullet['z'] += bullet_speed * math.cos(rad)

        if 0 <= bullet['x'] <= grid_size and 0 <= bullet['z'] <= grid_size:
            hit = False
            for j in enemies:
                dx = bullet['x'] - j['x']
                dz = bullet['z'] - j['z']
                if math.sqrt(dx * dx + dz * dz) < 0.5:
                    score += 10
                    enemies.remove(j)
                    hit = True
                    break
            if not hit:
                new_bullets.append(bullet)
        else:
            if not cheat_mode:
                missed_bullets += 1
                print(f"Bullet missed: {missed_bullets}")
    bullets = new_bullets

def fcheat_mode():
    global player_angle, cheat_index, bullets, cooldown
    player_angle_increment = 2
    player_angle = (player_angle + player_angle_increment) % 360
    if cooldown > 0:
        cooldown -= 1

    if cooldown == 0 and len(enemies) > 0:
        target = enemies[cheat_index % len(enemies)]
        dx = target['x'] - player_x
        dz = target['z'] - player_z
        angle = math.degrees(math.atan2(dx, dz))
        bullets.append({
            'x': player_x,
            'z': player_z,
            'angle': angle
        })
        cheat_index += 1
        cooldown = 60

def restart_game():
    global score, lives, missed_bullets, game_over, bullets,player_x, player_z, player_angle,camera_mode
    score = 0
    lives = 5
    missed_bullets = 0
    game_over = False
    player_x = grid_size / 2
    player_z = grid_size / 2
    player_angle = 0
    camera_mode="3rd"
    bullets.clear()
    spawn_enemies()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if camera_mode == "3rd":
        cam_x = grid_size / 2 + camera_radius * math.sin(math.radians(camera_angle))
        cam_z = grid_size / 2 + camera_radius * math.cos(math.radians(camera_angle))
        gluLookAt(cam_x, camera_height, cam_z, grid_size / 2, 0, grid_size / 2, 0, 1, 0)
    else:
        rad = math.radians(player_angle)
        x = player_x
        y =  1
        z = player_z
        center_x = x + math.sin(rad)
        center_y = y
        center_z = z + math.cos(rad)
        gluLookAt(x, y, z, center_x, center_y, center_z, 0, 1, 0)

    draw_grid()
    draw_walls()
    draw_player()
    draw_bullets()
    draw_enemies()

    if not game_over:
        update_bullets()
        update_enemies()
        gameover()

    glDisable(GL_LIGHTING)

    if game_over:
        glColor3f(1, 0, 0)
        draw_text(10, 770, f"GAME OVER. Your Score is {score}", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 750, "Press 'R' to Restart the Game", GLUT_BITMAP_TIMES_ROMAN_24)
    else:
        glColor3f(1, 1, 1)
        draw_text(10, 770, f"Game Score: {score}",GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 750, f"Player life remaining: {lives}",GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 730, f"Player Bullet Missed: {missed_bullets}",GLUT_BITMAP_TIMES_ROMAN_24)
    glutSwapBuffers()
    glutPostRedisplay()

def gameover():
    global game_over, lives, missed_bullets
    if lives <= 0 or missed_bullets >= 10:
        game_over = True


def update_enemies():
    global lives, enemies, game_over

    for enemy in enemies[:]:
        move_enemy(enemy)
        animate_enemy(enemy)

        dx = enemy['x'] - player_x
        dz = enemy['z'] - player_z
        if (dx ** 2 + dz ** 2) ** 0.5 < 0.5:
            if lives > 0:
                lives -= 1
                print(f"Remaining player life: {lives}")
            enemies.remove(enemy)

    while len(enemies) < 5:
        enemies.append(respawn_enemy())

    gameover()

def move_enemy(enemy):
    dx = player_x - enemy['x']
    dz = player_z - enemy['z']
    dist = math.hypot(dx, dz)
    if dist > 0:
        enemy['x'] += 0.001 * dx / dist
        enemy['z'] += 0.001 * dz / dist

def animate_enemy(enemy):
    if enemy['shrinking']:
        enemy['scale'] -= 0.002
        if enemy['scale'] <= 0.6:
            enemy['shrinking'] = False
    else:
        enemy['scale'] += 0.002
        if enemy['scale'] >= 1.2:
            enemy['shrinking'] = True


def respawn_enemy():
    while True:
        x = random.uniform(1, grid_size - 1)
        z = random.uniform(1, grid_size - 1)
        if abs(x - player_x) > 3 and abs(z - player_z) > 3:
            return {'x': x, 'z': z, 'scale': 1.0, 'shrinking': True}

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 1, 100)
    glMatrixMode(GL_MODELVIEW)


def spawn_enemies():
    global enemies
    enemies = []
    for _ in range(num_enemies):
        while True:
            x = random.uniform(1, grid_size - 1)
            z = random.uniform(1, grid_size - 1)
            if abs(x - player_x) > 2 and abs(z - player_z) > 2:
                enemies.append({'x': x, 'z': z, 'scale': 1.0, 'shrinking': True})
                break

def special_keys(key, x, y):
    global camera_angle, camera_radius,game_over,camera_height
    if game_over:
        return
    if key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle - 5) % 360
    elif key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle + 5) % 360
    elif key == GLUT_KEY_DOWN:
        camera_radius = min(camera_radius + 1, 30)
        camera_height = min(camera_height + 1, 20)
    elif key == GLUT_KEY_UP:
        camera_radius = max(camera_radius - 1, 10)
        camera_height = max(camera_height - 1, 12)
    glutPostRedisplay()

def keyboard(key, x, y):
    global player_x, player_z, player_angle, game_over, cheat_mode

    if game_over:
        if key == b'r':
            restart_game()
        return
    if key == b'c':
        cheat_mode = not cheat_mode
        return

    step = 0.2
    if key == b'w':
        rad = math.radians(player_angle)
        player_x += step * math.sin(rad)
        player_z += step * math.cos(rad)
    elif key == b's':
        rad = math.radians(player_angle)
        player_x -= step * math.sin(rad)
        player_z -= step * math.cos(rad)
    elif key == b'a':
        player_angle = (player_angle - 5) % 360
    elif key == b'd':
        player_angle = (player_angle + 5) % 360

    min_pos = 0.5
    max_pos = grid_size - 0.5
    player_x = max(min(player_x, max_pos), min_pos)
    player_z = max(min(player_z, max_pos), min_pos)

    glutPostRedisplay()

def mouse(button, state, x, y):
    global camera_mode
    if game_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print("Player Bullet fired!")
        bullets.append({
            'x': player_x,
            'z': player_z,
            'angle': player_angle
        })
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        # Toggle camera mode
        if camera_mode == "3rd":
            camera_mode = "1st"
        else:
            camera_mode = "3rd"
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Bullet Frenzy")
    init()
    glutDisplayFunc(display)
    spawn_enemies()
    glutReshapeFunc(reshape)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMainLoop()

if __name__ == "__main__":
    main()
