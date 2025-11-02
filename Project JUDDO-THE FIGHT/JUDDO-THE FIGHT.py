import math
import random
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ---------------------------
# 1. Configuration and Globals
# ---------------------------

# Window size (more landscape)
window_width, window_height = 1200.0, 800.0  # Updated size

# Game state variables
game_state = "Main Menu"  # Initial state set to Main Menu
players = []
score = [0, 0]
game_over_flags = [False, False]  # To track game over for each player
last_time = time.time()
coin_no = 0


# Round tracking
current_round = 1
total_rounds = 3
dead_characters = set()

# Button configurations for different menus
buttons = {
    "Main Menu": {
        "SinglePlayer": {
            "x_ratio": 0.5,
            "y_ratio": 0.6,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.349, 0.349, 0.349],
            "label": "Single Player"
        },
        "Multiplayer": {
            "x_ratio": 0.5,
            "y_ratio": 0.45,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.349, 0.349, 0.349],
            "label": "Multiplayer"
        },
        "Exit": {
            "x_ratio": 0.5,
            "y_ratio": 0.3,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.49, 0.129, 0.129],
            "label": "Exit"
        },
    },
    "CharacterSelect": {
        "Player1_Reety": {
            "x_ratio": 0.25,
            "y_ratio": 0.6,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.529, 0.247, 0.671],
            "label": "Reety"
        },
        "Player1_Argha": {
            "x_ratio": 0.25,
            "y_ratio": 0.45,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.263, 0.263, 0.541],
            "label": "Argha"
        },
        "Player1_Avishek": {
            "x_ratio": 0.25,
            "y_ratio": 0.3,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.008, 0.369, 0.62],
            "label": "Avishek"
        },

        "Player2_Reety": {
            "x_ratio": 0.75,
            "y_ratio": 0.6,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.529, 0.247, 0.671],
            "label": "Reety"
        },
        "Player2_Argha": {
            "x_ratio": 0.75,
            "y_ratio": 0.45,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.263, 0.263, 0.541],
            "label": "Argha"
        },
        "Player2_Avishek": {
            "x_ratio": 0.75,
            "y_ratio": 0.3,
            "width_ratio": 0.15,
            "height_ratio": 0.08,
            "color": [0.008, 0.369, 0.62],
            "label": "Avishek"
        },
        "Start": {  # Start button added
            "x_ratio": 0.5,
            "y_ratio": 0.15,
            "width_ratio": 0.2,
            "height_ratio": 0.08,
            "color": [0.3, 0.3, 0.3],  # Initially gray (inactive)
            "label": "Start",
            "enabled": False  # Custom flag to manage button state
        }
    },

    "CharacterSelectSingle": {
        "Reety": {
            "x_ratio": 0.5,
            "y_ratio": 0.6,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.529, 0.247, 0.671],
            "label": "Reety"
        },
        "Argha": {
            "x_ratio": 0.5,
            "y_ratio": 0.45,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.263, 0.263, 0.541],
            "label": "Argha"
        },
        "Avishek": {
            "x_ratio": 0.5,
            "y_ratio": 0.3,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.008, 0.369, 0.62],
            "label": "Avishek"
        },
        "Start": {  # Start button added
            "x_ratio": 0.5,
            "y_ratio": 0.15,
            "width_ratio": 0.2,
            "height_ratio": 0.08,
            "color": [0.3, 0.3, 0.3],  # Initially gray (inactive)
            "label": "Start",
            "enabled": False  # Custom flag to manage button state
        },
    },

    "GameOver": {
        "BackToMain": {
            "x_ratio": 0.5,
            "y_ratio": 0.4,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.349, 0.349, 0.349],
            "label": "Main Menu"
        },
        "Exit": {
            "x_ratio": 0.5,
            "y_ratio": 0.25,
            "width_ratio": 0.25,
            "height_ratio": 0.08,
            "color": [0.49, 0.129, 0.129],
            "label": "Exit"
        },
    }
}

# Key handling
pressed_keys = set()

# Fonts for button labels
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18

# Mouse position
mouse_x, mouse_y = 0.0, 0.0

# Hover state
hover_buttons = set()

# Selected characters
selected_characters = {"Player1": None, "Player2": None}

# Obstacles
obstacles = []

# Coins
coins = []
coin_spawn_interval = 5.0  # Spawn a coin every 5 seconds
last_coin_spawn_time = time.time()

# Thruster trails for players
thruster_trails = {"Player1": [], "Player2": []}

# ---------------------------
# 2. Helper Functions
# ---------------------------
def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6


def all_zone_to_zone_0(x, y, zone):
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


def zero_to_zone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 6:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 2:
        return -y, x
    elif zone == 7:
        return x, -y


def draw8way(x, y, zone):
    points = [
        (x, y),
        (y, x),
        (-x, y),
        (x, -y),
        (-x, -y),
        (-y, x),
        (y, -x),
        (-y, -x)
    ]
    rotation_angle = zone * 45  # Each zone represents a 45-degree rotation
    rotated_points = []
    rad = math.radians(rotation_angle)
    cos_theta = math.cos(rad)
    sin_theta = math.sin(rad)
    for px, py in points:
        rx = px * cos_theta - py * sin_theta
        ry = px * sin_theta + py * cos_theta
        rotated_points.append((float(rx), float(ry)))
    return rotated_points


def get_line_points(x0, y0, x1, y1):
    zone = findZone(x0, y0, x1, y1)
    x0_zone0, y0_zone0 = all_zone_to_zone_0(x0, y0, zone)
    x1_zone0, y1_zone0 = all_zone_to_zone_0(x1, y1, zone)

    dx = x1_zone0 - x0_zone0
    dy = y1_zone0 - y0_zone0

    d = 2.0 * dy - dx
    y = y0_zone0

    re_y = y0_zone0
    points = [(x0, y0)]
    for re_x in range(int(math.floor(x0_zone0)), int(math.floor(x1_zone0)) + 1):
        if d > 0:
            re_y += 1.0
            d += 2.0 * (dy - dx)
        else:
            d += 2.0 * dy
        fin_x, fin_y = zero_to_zone(float(re_x), float(re_y), zone)
        points.append((fin_x, fin_y))

    return points

# ---------------------------
# 3. Optimized Drawing Functions
# ---------------------------

def draw_line_custom(x0, y0, x1, y1, color):
    glColor3f(*color)
    glBegin(GL_POINTS)

    zone = findZone(x0, y0, x1, y1)
    x0_zone0, y0_zone0 = all_zone_to_zone_0(x0, y0, zone)
    x1_zone0, y1_zone0 = all_zone_to_zone_0(x1, y1, zone)

    dx = x1_zone0 - x0_zone0
    dy = y1_zone0 - y0_zone0

    d = 2.0 * dy - dx
    y = y0_zone0

    re_y = y0_zone0
    for re_x in range(int(math.floor(x0_zone0)), int(math.floor(x1_zone0)) + 1):
        if d > 0:
            re_y += 1.0
            d += 2.0 * (dy - dx)
        else:
            d += 2.0 * dy
        fin_x, fin_y = zero_to_zone(float(re_x), float(re_y), zone)
        glVertex2f(fin_x, fin_y)
    glEnd()


def draw_circle(x_center, y_center, radius, color):
    glColor3f(*color[:3])  # Use RGB only
    glBegin(GL_POINTS)

    x = 0.0
    y = float(radius)
    d = 1.0 - float(radius)

    def plot_circle_points(xc, yc, x, y):
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)

    while x <= y:
        plot_circle_points(x_center, y_center, x, y)
        if d < 0:
            d += 2.0 * x + 3.0
        else:
            d += 2.0 * (x - y) + 5.0
            y -= 1.0
        x += 1.0
    glEnd()


def draw_ball(x, y, radius, color):
    for i in range(1, int(radius) + 1):
        draw_circle(x, y, float(i), color)


def draw_rectangle(x1, y1, x2, y2, color):
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x_min, y_min)
    glVertex2f(x_max, y_min)
    glVertex2f(x_max, y_max)
    glVertex2f(x_min, y_max)
    glEnd()


def draw_poly(p1, p2, p3, p4, color):
    # clockwise or anticlockwise
    line1 = get_line_points(p1[0], p1[1], p2[0], p2[1])
    for i in line1:
        draw_line_custom(i[0], i[1], p4[0], p4[1], color)

    line2 = get_line_points(p3[0], p3[1], p4[0], p4[1])
    for i in line2:
        draw_line_custom(i[0], i[1], p2[0], p2[1], color)


def draw_tri(p1, p2, p3, color):
    line1 = get_line_points(p1[0], p1[1], p2[0], p2[1])
    print(line1)
    for i in line1:
        draw_line_custom(i[0], i[1], p3[0], p3[1], color)


from OpenGL.GL import *


def draw_transparent_line(x0, y0, x1, y1, color, alpha=1.0, ):
    glPointSize(5.0)  # Set the size of each point
    glBegin(GL_POINTS)

    steps = int(max(abs(x1 - x0), abs(y1 - y0)))
    for i in range(steps + 1):
        t = i / steps  # Normalize step to a value between 0 and 1
        current_alpha = alpha * (1 - t)  # Gradually decrease alpha from start to 0

        glColor4f(color[0], color[1], color[2], current_alpha)

        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)

        glVertex2f(x, y)

    glEnd()

    # Reset color to opaque white to avoid affecting other drawings
    glPointSize(2)
    glColor3f(1.0, 1.0, 1.0)


def draw_uzi(x, y, size=0.25, angle=0.0, mirror=False):
    """
    Draws a smaller and rotatable uzi gun at the specified (x, y) position.
    Args:
        x (float): X-coordinate of the uzi's base position.
        y (float): Y-coordinate of the uzi's base position.
        size (float): Scaling factor for the uzi's size.
        angle (float): Rotation angle in degrees.
        mirror (bool): If True, mirror the uzi horizontally.
    """
    glPushMatrix()
    glTranslatef(float(x), float(y), 0.0)
    if mirror:
        glScalef(-1.0, 1.0, 1.0)  # Mirror horizontally
    glRotatef(float(angle), 0.0, 0.0, 1.0)  # Rotate based on aim angle
    glScalef(float(size), float(size), 1.0)  # Scale the uzi down

    # Changed jetpack color and added glowing effect
    gray = (0.388, 0.388, 0.388)
    dark_gray = (0.688, 0.688, 0.688)
    glowing_color = (1.0, 1.0, 0.0)  # Yellow for glowing parts

    # Base of the uzi
    draw_poly(
        (-103.0, 24.0),
        (-95.0, 24.0),
        (-83.0, 13.0),
        (-103.0, 13.0),
        dark_gray
    )

    # Middle parts
    draw_poly(
        (-103.0, -13.0),
        (-99.0, -13.0),
        (-100.0, -28.0),
        (-103.0, -36.0),
        dark_gray
    )
    draw_poly(
        (-99.0, -13.0),
        (-88.0, -13.0),
        (-90.0, -16.0),
        (-100.0, -20.0),
        dark_gray
    )

    # Body
    draw_rectangle(
        -104.0, 13.0,
        17.0, -13.0,
        gray
    )

    # Top part
    draw_poly(
        (95.0, 24.0),
        (100.0, 24.0),
        (100.0, 2.0),
        (80.0, 2.0),
        dark_gray
    )
    draw_rectangle(
        17.0, 13.0,
        87.0, 2.0,
        gray
    )
    draw_rectangle(
        17.0, 2.0,
        100.0, -15.0,
        (0.2, 0.2, 0.2)
    )

    # Barrel with glowing effect
    draw_rectangle(
        100.0, 9.0,
        105.0, 2.0,
        gray
    )
    draw_rectangle(
        102.0, 11.0,
        110.0, 0.0,
        dark_gray
    )
    # Glowing part
    draw_transparent_line(
        105.0, 5.0,
        115.0, 5.0,
        glowing_color,
        alpha=0.7
    )

    # Handle
    draw_rectangle(
        -40.0, -13.0,
        -14.0, -63.0,
        gray
    )

    # Stock
    draw_rectangle(
        -14.0, -28.0,
        14.0, -31.0,
        gray
    )
    draw_rectangle(
        14.0, -31.0,
        17.0, -13.0,
        gray
    )

    # Magazine
    draw_rectangle(
        -37.0, -120.0,
        -16.0, -63.0,
        dark_gray
    )

    glPopMatrix()

# ---------------------------
# 4. Stickman Drawing Function
# ---------------------------

def draw_stickman(x, y, color, aim_angle, has_uzi=True, size=1.0, mirror=False, thruster_phase=0.0, player_id="Player1"):
    """
    Draws an enhanced stickman figure with thrusters and an uzi.

    Args:
        x (float): X-coordinate of the stickman's center.
        y (float): Y-coordinate of the stickman's center.
        color (list): RGB color list for the stickman.
        aim_angle (float): Angle at which the stickman is aiming.
        has_uzi (bool): Flag to determine if the stickman holds an uzi.
        size (float): Scaling factor for the stickman's size.
        mirror (bool): If True, mirror the stickman horizontally (useful for Player 2).
        thruster_phase (float): Current phase for thruster animation.
        player_id (str): Identifier for the player ("Player1" or "Player2") to manage thruster trails.
    """
    glPushMatrix()
    glTranslatef(float(x), float(y), 0.0)
    if mirror:
        glScalef(-1.0, 1.0, 1.0)  # Mirror horizontally
    glScalef(float(size), float(size), 1.0)  # Scale the stickman

    glColor3f(*color)

    # Head
    head_radius = 10.0
    draw_ball(0.0, 40.0, head_radius, color)

    # Body
    glBegin(GL_LINES)
    glVertex2f(0.0, 30.0)
    glVertex2f(0.0, -30.0)
    glEnd()

    # Arms
    arm_length = 20.0
    left_arm_x = -arm_length
    right_arm_x = arm_length
    glBegin(GL_LINES)
    glVertex2f(0.0, 20.0)
    glVertex2f(left_arm_x, 0.0)
    glVertex2f(0.0, 20.0)
    glVertex2f(right_arm_x, 0.0)
    glEnd()

    # Legs
    leg_length = 20.0
    glBegin(GL_LINES)
    glVertex2f(0.0, -30.0)
    glVertex2f(-15.0, -50.0)
    glVertex2f(0.0, -30.0)
    glVertex2f(15.0, -50.0)
    glEnd()

    # Thrusters (Jet Shoes) at feet fixed position with trail
    thruster_size = 5.0
    thruster_offset_y = -50.0  # Fixed position

    glPointSize(thruster_size)

    thruster_color = (1, 1, 1)  # Green color for thrusters
    # Left thruster
    draw_transparent_line(-15.0, thruster_offset_y, -15.0, thruster_offset_y - 20.0, thruster_color, alpha=0.7)
    # Right thruster
    draw_transparent_line(15.0, thruster_offset_y, 15.0, thruster_offset_y - 20.0, thruster_color, alpha=0.7)

    # Draw Uzi in the right hand if the stickman has one
    if has_uzi:
        # The uzi should be drawn relative to the right arm's end position (0.0, 0.0)
        # Adjust aim_angle for correct initial rotation
        if mirror:
            adjusted_aim_angle = aim_angle - 180.0  # Reflect the angle for mirrored stickman
        else:
            adjusted_aim_angle = aim_angle
        draw_uzi(right_arm_x, 0.0, size=0.25, angle=adjusted_aim_angle, mirror=mirror)

    glPopMatrix()

# ---------------------------
# 5. Player and AI Class Definitions
# ---------------------------

class Player:
    def __init__(self, x, y, color, controls, half, is_ai=False):
        self.x = float(x)
        self.y = float(y)
        self.initial_x = float(x)
        self.initial_y = float(y)
        self.color = color  # RGB list
        self.width = 40.0
        self.height = 80.0  # Increased height for better collision
        self.projectiles = []
        self.abilities = []
        self.controls = controls  # Dictionary mapping keys to actions
        self.score = 0
        self.game_over = False
        self.health = 100.0  # Default health, will be set based on character
        self.ability_cooldown = 5.0  # seconds
        self.last_ability_time = 0.0
        self.shield_active = False
        self.shield_duration = 3.0  # seconds
        self.shield_end_time = 0.0
        self.aim_line_length = 150.0  # Default aim line length
        self.aim_angle = 0.0  # Angle in degrees
        self.half = half  # 'left' or 'right'
        self.selected_character_type = None
        self.selected_character_set = set()
        self.is_ai = is_ai
        self.ai_last_shot_time = 0.0
        self.ai_shot_interval = 1.0  # AI shoots every 1 second
        self.thruster_phase = 0.0  # For thruster animation
        self.firerate = 1.0  # Default firerate, will be set based on character
        self.last_shot_time = 0.0  # To control firerate

        # Initialize aim_angle based on player's half
        if self.half == 'left':
            self.aim_angle = 0.0  # Facing right
        else:
            self.aim_angle = -180.0  # Facing left

    def set_character(self, type):
        self.selected_character_type = Character(type)
        self.health = float(self.selected_character_type.health)
        self.firerate = float(self.selected_character_type.firerate)
        self.selected_character_set.add(type)

    def move(self, direction, delta_time=1.0):
        # Movement speed based on character's speed attribute
        speed = self.selected_character_type.speed * 100.0 * delta_time  # Pixels per second

        # Store previous position before moving
        self.prev_x = self.x
        self.prev_y = self.y

        if direction == 'up':
            self.y += speed
            if self.y + self.height / 2.0 > window_height:
                self.y = window_height - self.height / 2.0
        elif direction == 'down':
            self.y -= speed
            if self.y - self.height / 2.0 < 0.0:
                self.y = self.height / 2.0
        elif direction == 'left':
            self.x -= speed
            if self.half == 'left' and self.x - self.width / 2.0 < 0.0:
                self.x = self.width / 2.0
            elif self.half == 'right' and self.x - self.width / 2.0 < window_width / 2.0:
                self.x = window_width / 2.0 + self.width / 2.0
        elif direction == 'right':
            self.x += speed
            if self.half == 'left' and self.x + self.width / 2.0 > window_width / 2.0:
                self.x = window_width / 2.0 - self.width / 2.0
            elif self.half == 'right' and self.x + self.width / 2.0 > window_width:
                self.x = window_width - self.width / 2.0

    def shoot(self, target_x, target_y):
        current_time = time.time()
        if current_time - self.last_shot_time >= self.firerate:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)
            if distance == 0:
                return
            dx /= distance
            dy /= distance
            speed = 500.0  # pixels per second
            self.projectiles.append({
                "x": self.x,
                "y": self.y,
                "dx": dx,
                "dy": dy,
                "speed": speed,
                "damage": self.selected_character_type.damage
            })
            self.last_shot_time = current_time

    def activate_ability(self, current_time):
        if current_time - self.last_ability_time >= self.ability_cooldown:
            if self.selected_character_type.special == "Rage":
                self.enable_rapid_fire()
            elif self.selected_character_type.special == "Shield":
                self.activate_shield(current_time)
            self.last_ability_time = current_time

    def enable_rapid_fire(self):
        # Example: Reduce firerate for rapid fire
        self.firerate = max(self.firerate / 2.0, 0.25)  # Minimum firerate
        print(f"{self.selected_character_type.name} activated Rapid Fire!")

    def activate_shield(self, current_time):
        self.shield_active = True
        self.shield_end_time = current_time + self.shield_duration
        print(f"{self.selected_character_type.name} activated Shield!")

    def increase_aim_line(self):
        self.aim_line_length = min(self.aim_line_length + 20.0, 300.0)  # Max length 300

    def decrease_aim_line(self):
        self.aim_line_length = max(self.aim_line_length - 20.0, 50.0)  # Min length 50

    def adjust_aim_angle(self, delta):
        self.aim_angle += delta
        if self.half == 'left':
            if self.aim_angle > 90.0:
                self.aim_angle = 90.0
            elif self.aim_angle < -90.0:
                self.aim_angle = -90.0
        else:
            if self.aim_angle > 270.0:
                self.aim_angle = 270.0
            elif self.aim_angle < 90.0:
                self.aim_angle = 90.0

    def update(self, delta_time, current_time):
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile['x'] += projectile['dx'] * projectile['speed'] * delta_time
            projectile['y'] += projectile['dy'] * projectile['speed'] * delta_time
            # Remove projectile if it goes out of bounds
            if (projectile['y'] > window_height or projectile['y'] < 0.0 or
                    projectile['x'] > window_width or projectile['x'] < 0.0):
                self.projectiles.remove(projectile)

        # Update shield status
        if self.shield_active and current_time >= self.shield_end_time:
            self.shield_active = False
            # Reset firerate after shield ends if rapid fire was enabled
            if self.selected_character_type.special == "Rage":
                self.firerate = self.selected_character_type.firerate

        # Update thruster animation phase
        self.thruster_phase += delta_time
        if self.thruster_phase > 2.0 * math.pi:
            self.thruster_phase -= 2.0 * math.pi

        # AI Behavior
        if self.is_ai and not self.game_over:
            self.ai_behavior(delta_time, current_time)

    def ai_behavior(self, delta_time, current_time):
        self.prev_x = self.x
        self.prev_y = self.y

        global window_width, window_height

        # Enhanced AI: Move towards the player, avoid obstacles, and shoot intelligently
        player = players[0]  # Assuming Player1 is the human player
        direction_x = player.x - self.x
        direction_y = player.y - self.y
        distance = math.hypot(direction_x, direction_y)




        # Normalize direction
        if distance != 0.0:
            direction_x /= distance
            direction_y /= distance

            # Simple obstacle avoidance
            avoid_x, avoid_y = 0.0, 0.0
            for obstacle in obstacles:
                # Check if the AI is near an obstacle
                obstacle_center_x = obstacle.x + obstacle.width / 2.0
                obstacle_center_y = obstacle.y + obstacle.height / 2.0
                buffer_distance = 50.0  # Buffer to start avoiding
                dx = obstacle_center_x - self.x
                dy = obstacle_center_y - self.y
                dist_to_obstacle = math.hypot(dx, dy)
                if dist_to_obstacle < (obstacle.width / 2.0 + buffer_distance) and dist_to_obstacle != 0:
                    avoid_x -= dx / dist_to_obstacle
                    avoid_y -= dy / dist_to_obstacle

            # Combine movement directions
            move_x = direction_x + avoid_x * 0.05
            move_y = direction_y + avoid_y * 0.05
            move_distance = math.hypot(move_x, move_y)
            if move_distance != 0:
                move_x /= move_distance
                move_y /= move_distance


        # Move towards the player with slight avoidance
        speed = self.selected_character_type.speed  # AI movement speed


        self.x += move_x * speed
        self.y += move_y * speed

        # Clamp position within bounds
        self.x = min(window_width , max(self.x, window_width / 2.0))
        self.y = max(0, min(int(self.y), int(window_height)))


        # Aim towards the player
        self.aim_angle = math.degrees(math.atan2(player.y - self.y, player.x - self.x))

        # Shoot at intervals based on distance
        if current_time - self.ai_last_shot_time >= self.ai_shot_interval:
            if distance < 1200:  # AI shoots only if player is within 400 pixels
                self.shoot(player.x, player.y)
                self.ai_last_shot_time = current_time

    def draw(self):
        """
        Draws the player as an enhanced stickman with an uzi and animated thrusters.
        """
        if self.half == 'left':
            mirror = False
            player_id = "Player1"
        else:
            mirror = True
            player_id = "Player2"
        draw_stickman(
            x=self.x,
            y=self.y,
            color=self.selected_character_type.color,
            aim_angle=self.aim_angle,
            has_uzi=True,
            size=1.0,  # Adjust size as needed
            mirror=mirror,
            thruster_phase=self.thruster_phase,
            player_id=player_id
        )

class Character:
    def __init__(self, type):
        if type == "Reety":
            self.name = 'Reety'
            self.health = 100
            self.gun = 'uzi'
            self.damage = 19
            self.speed = 2.0
            self.firerate = 0.25
            self.special = "Rage"
            self.color = [0.529, 0.247, 0.671]

        elif type == "Argha":
            self.name = 'Argha'
            self.health = 100
            self.gun = 'scar'
            self.damage = 20
            self.speed = 2.5
            self.firerate = 0.5
            self.special = "Gun-jam"
            self.color = [0.263, 0.263, 0.541]

        elif type == "Avishek":
            self.name = 'Avishek'
            self.health = 125
            self.gun = 'sniper'
            self.damage = 50
            self.speed = 1.75
            self.firerate = 0.75
            self.special = "Laser"
            self.color = [0.008, 0.369, 0.62]

# ---------------------------
# 6. Obstacle Class Definition
# ---------------------------

class Obstacle:
    def __init__(self, x, y, width, height, color=(0.5, 0.5, 0.5)):
        """
        Initializes a rectangular obstacle.

        Args:
            x (float): X-coordinate of the obstacle's bottom-left corner.
            y (float): Y-coordinate of the obstacle's bottom-left corner.
            width (float): Width of the obstacle.
            height (float): Height of the obstacle.
            color (tuple): RGB color tuple for the obstacle.
        """
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.color = color

    def draw(self):
        """
        Draws the rectangular obstacle on the screen.
        """
        draw_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            self.color
        )

    def check_collision_with_point(self, px, py):
        """
        Checks if a point (px, py) is inside the obstacle.

        Args:
            px (float): X-coordinate of the point.
            py (float): Y-coordinate of the point.

        Returns:
            bool: True if the point is inside the obstacle, False otherwise.
        """
        return (self.x <= px <= self.x + self.width) and (self.y <= py <= self.y + self.height)

# ---------------------------
# 7. Coin Class Definition
# ---------------------------

class Coin:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 10.0  # Radius of the coin
        self.color = (0.871, 0.733, 0.129) # Yellow color

    def draw(self):
        draw_ball(self.x, self.y, self.radius, self.color)

# ---------------------------
# 8. Drawing Functions for UI
# ---------------------------

def draw_button(btn):
    """
    Draw a single button with its label.
    Adds visual feedback if the button is hovered or active.
    """
    x_ratio, y_ratio = btn["x_ratio"], btn["y_ratio"]
    width_ratio, height_ratio = btn["width_ratio"], btn["height_ratio"]
    color = btn["color"]
    label = btn.get("label", "")
    enabled = btn.get("enabled", True)  # Default to True if not specified

    # Calculate actual positions based on window size
    x = x_ratio * window_width - (btn["width_ratio"] * window_width) / 2.0
    y = y_ratio * window_height - (btn["height_ratio"] * window_height) / 2.0
    width = btn["width_ratio"] * window_width
    height = btn["height_ratio"] * window_height

    # Check if button is hovered
    is_hovered = btn.get("name") in hover_buttons

    # Determine button color based on state
    if not enabled:
        display_color = [0.3, 0.3, 0.3]  # Gray color for inactive buttons
    else:
        display_color = color.copy()

    if is_hovered and enabled:
        # Change color intensity for hover effect
        display_color = [min(c + 0.3, 1.0) for c in display_color]

    # Draw button rectangle
    draw_rectangle(x, y, x + width, y + height, display_color)

    # Draw button border for better visibility
    border_color = [1.0, 1.0, 1.0] if is_hovered and enabled else [0.0, 0.0, 0.0]
    glColor3f(*border_color)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()
    glLineWidth(1.0)  # Reset to default

    # Draw the button label
    glColor3f(1.0, 1.0, 1.0)  # White color for text
    text_width = len(label) * 8.0  # Approximate width
    glRasterPos2f(x + (width - text_width) / 2.0, y + height / 2.0 - 8.0)  # Centered text
    for char in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_buttons(menu):
    """
    Draw all buttons for the given menu.
    Adds visual feedback if the button is hovered.
    """
    if menu not in buttons:
        return

    for btn_name, btn in buttons[menu].items():
        btn_copy = btn.copy()
        btn_copy["name"] = btn_name.strip()

        # Manage the enabled state for the Start button
        if btn_name == "Start":
            if menu == "CharacterSelect":
                # Enabled only if both players have selected their characters
                if selected_characters["Player1"] and selected_characters["Player2"]:
                    btn_copy["enabled"] = True
                    btn_copy["color"] = [0.008, 0.478, 0.031]  # Green when enabled
                else:
                    btn_copy["enabled"] = False
            elif menu == "CharacterSelectSingle":
                # Enabled only if Player1 has selected a character
                if selected_characters["Player1"]:
                    btn_copy["enabled"] = True
                    btn_copy["color"] = [0.008, 0.478, 0.031]  # Green when enabled
                else:
                    btn_copy["enabled"] = False

        # Grey out buttons for dead characters
        if menu in ["CharacterSelect", "CharacterSelectSingle"]:
            character_label = btn_copy.get("label", "")
            if character_label in dead_characters:
                btn_copy["enabled"] = False
                btn_copy["color"] = [0.3, 0.3, 0.3]  # Grey color

        draw_button(btn_copy)


def draw_game_over_text(winner_text=""):
    """
    Draw 'Game Over' or 'Congratulations' text on the screen.
    """
    if winner_text:
        text = winner_text
        glColor3f(0.0, 1.0, 0.0)  # Green color for congratulations
    else:
        text = "Game Over"
        glColor3f(1.0, 0.0, 0.0)  # Red color

    glRasterPos2f(window_width / 2.0 - 80.0, window_height * 0.8)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_main_menu_text():
    """
    Draw 'Main Menu' title on the screen.
    """
    glColor3f(1.0, 1.0, 1.0)  # White color
    glRasterPos2f(window_width / 2.0 - 40.0, window_height * 0.8)
    for char in "Main Menu":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_character_select_text():
    """
    Draw 'Select Character' title on the screen.
    """
    glColor3f(1.0, 1.0, 1.0)  # White color
    glRasterPos2f(window_width / 2.0 - 80.0, window_height * 0.8)
    for char in "Select Character":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_selected_characters():
    """
    Display selected characters for both players.
    """
    glColor3f(1.0, 1.0, 1.0)  # White color
    # Player 1
    glRasterPos2f(window_width * 0.1 - 50.0, window_height * 0.9)
    for char in "Player 1 Selected:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    selected = selected_characters["Player1"] if selected_characters["Player1"] else "None"
    glRasterPos2f(window_width * 0.1 + 105.0, window_height * 0.9)
    for char in selected:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Player 2
    glRasterPos2f(window_width * 0.75 - 50.0, window_height * 0.9)
    for char in "Player 2 Selected:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    selected = selected_characters["Player2"] if selected_characters["Player2"] else "None"
    glRasterPos2f(window_width * 0.75 + 105.0, window_height * 0.9)
    for char in selected:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_selected_characters_single():
    """
    Display selected characters for Player 1 and the Computer (Player 2).
    """
    glColor3f(1.0, 1.0, 1.0)  # White color
    # Player 1
    glRasterPos2f(window_width * 0.1 - 50.0, window_height * 0.9)
    for char in "Player 1 Selected:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    selected = selected_characters["Player1"] if selected_characters["Player1"] else "None"
    glRasterPos2f(window_width * 0.1 + 105.0, window_height * 0.9)
    for char in selected:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Computer (Player 2)
    glRasterPos2f(window_width * 0.75 - 50.0, window_height * 0.9)
    for char in "Computer Selected:":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    selected = selected_characters["Player2"] if selected_characters["Player2"] else "None"
    glRasterPos2f(window_width * 0.75 + 105.0, window_height * 0.9)
    for char in selected:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))


def draw_gameplay_ui():



    """
    Draw the UI elements during gameplay, such as scores and health.
    """

    global coin_no
    # Display scores and health
    glColor3f(0, 0, 0)  # White color

    # Player 1 Score, Health, and Type
    glRasterPos2f(window_width * 0.05, window_height * 0.95)
    character_p1 = players[0].selected_character_type.name if players[0].selected_character_type else "None"
    score_health_p1 = f"P1 ({character_p1}) Score: {players[0].score} | Health: {int(players[0].health)}"
    for char in score_health_p1:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Player 2 Score, Health, and Type
    glRasterPos2f(window_width * 0.7, window_height * 0.95)
    character_p2 = players[1].selected_character_type.name if players[1].selected_character_type else "None"
    score_health_p2 = f"P2 ({character_p2}) Score: {players[1].score} | Health: {int(players[1].health)}"
    for char in score_health_p2:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Display Current Round
    glRasterPos2f(window_width / 2.0 - 50.0, window_height * 0.95)
    round_text = f"Round: {current_round} / {total_rounds}"
    for char in round_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Display Coins Count
    glRasterPos2f(window_width / 2.0 - 50.0, window_height * 0.05)
    coins_text = f"Coins on Screen: {coin_no}"
    glColor3f(0.631, 0.565, 0.282)  # Yellow color for coins count
    for char in coins_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    glColor3f(1, 1, 1)  # Reset color to white

# ---------------------------
# 9. Button Click Detection and Hover Handling
# ---------------------------

def is_button_clicked(btn, x, y):
    """
    Simple bounding box check for button clicks.
    """
    btn_x = btn["x_ratio"] * window_width - (btn["width_ratio"] * window_width) / 2.0
    btn_y = btn["y_ratio"] * window_height - (btn["height_ratio"] * window_height) / 2.0
    btn_width = btn["width_ratio"] * window_width
    btn_height = btn["height_ratio"] * window_height
    return btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height


def keyboard_key_up(key, x, y):
    global pressed_keys
    pressed_keys.discard(key.lower())


def handle_hover(x, y):
    """
    Update hover_buttons set based on current mouse position.
    """
    global hover_buttons
    hover_buttons.clear()
    # Check all buttons in the current menu
    current_menu = game_state
    if current_menu in ["CharacterSelect", "CharacterSelectSingle"]:
        for btn_name, btn in buttons[current_menu].items():
            btn_x = btn["x_ratio"] * window_width - (btn["width_ratio"] * window_width) / 2.0
            btn_y = btn["y_ratio"] * window_height - (btn["height_ratio"] * window_height) / 2.0
            btn_width = btn["width_ratio"] * window_width
            btn_height = btn["height_ratio"] * window_height
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                # Only add to hover if the button is enabled and not a dead character
                if btn["label"] not in dead_characters:
                    if btn_name == "Start" and current_menu == "CharacterSelect":
                        if selected_characters["Player1"] and selected_characters["Player2"]:
                            hover_buttons.add(btn_name)
                    elif btn_name == "Start" and current_menu == "CharacterSelectSingle":
                        if selected_characters["Player1"]:
                            hover_buttons.add(btn_name)
                    elif btn_name.startswith("Player1_") or btn_name.startswith("Player2_"):
                        character = btn["label"]
                        if character not in dead_characters:
                            hover_buttons.add(btn_name)
    elif current_menu in ["Main Menu", "GameOver"]:
        for btn_name, btn in buttons[current_menu].items():
            btn_x = btn["x_ratio"] * window_width - (btn["width_ratio"] * window_width) / 2.0
            btn_y = btn["y_ratio"] * window_height - (btn["height_ratio"] * window_height) / 2.0
            btn_width = btn["width_ratio"] * window_width
            btn_height = btn["height_ratio"] * window_height
            if btn_x <= x <= btn_x + btn_width and btn_y <= y <= btn_y + btn_height:
                hover_buttons.add(btn_name)

def keyboard_listener(key, x, y):
    """
    Handle keyboard inputs for player movements and actions.
    """
    global pressed_keys, game_state

    key = key.lower()
    pressed_keys.add(key)

    if game_state in ["Multiplayer", "Singleplayer"]:
        for idx, player in enumerate(players):
            if player.game_over:
                continue
            controls = player.controls
            if controls['up'] in pressed_keys or controls['Up'] in pressed_keys:
                if (controls['left'] in pressed_keys or controls['Left'] in pressed_keys or
                        controls['right'] in pressed_keys or controls['Right'] in pressed_keys):
                    player.move('up', delta_time=0.016)  # Assuming ~60 FPS
                else:
                    player.move('up', delta_time=0.016)
            if controls['down'] in pressed_keys or controls['Down'] in pressed_keys:
                if (controls['left'] in pressed_keys or controls['Left'] in pressed_keys or
                        controls['right'] in pressed_keys or controls['Right'] in pressed_keys):
                    player.move('down', delta_time=0.016)
                else:
                    player.move('down', delta_time=0.016)
            if controls['left'] in pressed_keys or controls['Left'] in pressed_keys:
                if (controls['up'] in pressed_keys or controls['Up'] in pressed_keys or
                        controls['down'] in pressed_keys or controls['Down'] in pressed_keys):
                    player.move('left', delta_time=0.016)
                else:
                    player.move('left', delta_time=0.016)
            if controls['right'] in pressed_keys or controls['Right'] in pressed_keys:
                if (controls['up'] in pressed_keys or controls['Up'] in pressed_keys or
                        controls['down'] in pressed_keys or controls['Down'] in pressed_keys):
                    player.move('right', delta_time=0.016)
                else:
                    player.move('right', delta_time=0.016)
            if key == controls['shoot']:
                # Shoot towards the end of the aiming line based on aim_angle
                aim_radians = math.radians(player.aim_angle)
                end_x = player.x + math.cos(aim_radians) * player.aim_line_length
                end_y = player.y + math.sin(aim_radians) * player.aim_line_length
                player.shoot(end_x, end_y)
            if key == controls['aim_up'] or key == controls['Aim_up']:
                player.adjust_aim_angle(5.0)  # Move aim upwards by 5 degrees
            if key == controls['aim_down'] or key == controls['Aim_down']:
                player.adjust_aim_angle(-5.0)  # Move aim downwards by 5 degrees

def special_keyboard_listener(key, x, y):
    """
    Handle special keyboard inputs (like arrow keys) for Player 2.
    Currently not used but can be expanded if needed.
    """
    pass

def mouse_listener(button, state, x, y):
    """
    Handle mouse clicks for button interactions and shooting.
    """
    global game_over_flags, game_state

    if state == GLUT_DOWN:
        y_converted = float(window_height) - float(y)  # Convert to OpenGL coordinates
        if game_state == "Main Menu":
            for btn_name, btn in buttons["Main Menu"].items():
                btn_copy = btn.copy()
                btn_copy["name"] = btn_name
                if is_button_clicked(btn_copy, float(x), y_converted):
                    if btn_name == "SinglePlayer":
                        game_state = "CharacterSelectSingle"
                        selected_characters["Player1"] = None
                        selected_characters["Player2"] = None
                        print("Switched to Character Select Menu (Single Player)")
                    elif btn_name == "Multiplayer":
                        game_state = "CharacterSelect"
                        selected_characters["Player1"] = None
                        selected_characters["Player2"] = None
                        print("Switched to Character Select Menu (Multiplayer)")
                    elif btn_name == "Exit":
                        print("Exiting Game")
                        glutLeaveMainLoop()
        elif game_state == "CharacterSelect":
            for btn_name, btn in buttons["CharacterSelect"].items():
                btn_copy = btn.copy()
                btn_copy["name"] = btn_name.strip()
                if btn_name != "Start" and is_button_clicked(btn_copy, float(x), y_converted):
                    if btn_name.startswith("Player1_"):
                        character = btn_name.split("_")[1]
                        if character not in dead_characters:
                            selected_characters["Player1"] = character
                            print(f"Player 1 selected {selected_characters['Player1']}")
                    elif btn_name.startswith("Player2_"):
                        character = btn_name.split("_")[1]
                        if character not in dead_characters:
                            selected_characters["Player2"] = character
                            print(f"Player 2 selected {selected_characters['Player2']}")
            # Handle Start button click
            start_btn = buttons["CharacterSelect"].get("Start")
            if start_btn and is_button_clicked(start_btn, float(x), y_converted):
                if selected_characters["Player1"] and selected_characters["Player2"]:
                    initialize_players(selected_characters_list=[
                        selected_characters["Player1"],
                        selected_characters["Player2"]
                    ], is_singleplayer=False)
                    game_state = "Multiplayer"
                    print("Starting Multiplayer Game")
        elif game_state == "CharacterSelectSingle":
            for btn_name, btn in buttons["CharacterSelectSingle"].items():
                btn_copy = btn.copy()
                btn_copy["name"] = btn_name
                if btn_name != "Start" and is_button_clicked(btn_copy, float(x), y_converted):
                    character = btn_name
                    if character not in dead_characters:
                        selected_characters["Player1"] = character
                        # Assign Player2 (AI) character
                        available_characters = ['Reety', 'Argha', 'Avishek']
                        available_characters = [c for c in available_characters if c not in dead_characters]
                        if available_characters:
                            selected_ai_character = random.choice(available_characters)
                            selected_characters["Player2"] = selected_ai_character
                            print(f"Player 1 selected {selected_characters['Player1']}")
                            print(f"Computer selected {selected_characters['Player2']}")
            # Handle Start button click
            start_btn = buttons["CharacterSelectSingle"].get("Start")
            if start_btn and is_button_clicked(start_btn, float(x), y_converted):
                if selected_characters["Player1"]:
                    initialize_players(selected_characters_list=[
                        selected_characters["Player1"],
                        selected_characters["Player2"]
                    ], is_singleplayer=True)
                    game_state = "Singleplayer"
                    print("Starting Singleplayer Game")
        elif game_state in ["GameOver", "Final"]:
            for btn_name, btn in buttons["GameOver"].items():
                btn_copy = btn.copy()
                btn_copy["name"] = btn_name
                if is_button_clicked(btn_copy, float(x), y_converted):
                    if btn_name == "BackToMain":
                        reset_game()
                        initialize_players()
                        initialize_obstacles()
                        coins.clear()  # Clear all coins
                        game_over_flags[:] = [False, False]
                        game_state = "Main Menu"
                        print("Returned to Main Menu")
                    elif btn_name == "Exit":
                        print("Exiting Game")
                        glutLeaveMainLoop()
        elif game_state in ["Multiplayer", "Singleplayer"]:
            if button == GLUT_LEFT_BUTTON:
                if game_state == "Multiplayer":
                    player = players[1]  # Player2 in Multiplayer
                else:
                    player = players[0]  # Player1 in Singleplayer
                if not player.game_over:
                    aim_radians = math.radians(player.aim_angle)
                    end_x = player.x + math.cos(aim_radians) * player.aim_line_length
                    end_y = player.y + math.sin(aim_radians) * player.aim_line_length
                    player.shoot(end_x, end_y)

def mouse_motion_callback(x, y):
    """
    Handle passive mouse movements for button hover effects.
    """
    global mouse_x, mouse_y
    mouse_x = float(x)
    mouse_y = float(y)
    y_converted = float(window_height) - float(y)  # Convert to OpenGL coordinates
    handle_hover(float(x), y_converted)
    glutPostRedisplay()

# ---------------------------
# 10. Game Initialization
# ---------------------------

def initialize_players(selected_characters_list=None, is_singleplayer=False):
    """
    Initialize the players with their respective controls and positions.
    If selected_characters_list is provided, assign characters accordingly.

    Args:
        selected_characters_list (list): List of character names for Player1 and Player2.
        is_singleplayer (bool): Flag indicating if the game is in single-player mode.
    """
    global players
    if is_singleplayer:
        # Single Player Mode
        # Player1: Human Player on the left
        # Player2: AI on the right
        players = [
            Player(
                x=window_width / 4.0,  # Left side (25% of window width)
                y=100.0,
                color=[0.0, 1.0, 0.0],  # Green
                controls={
                    'up': b'w',
                    'down': b's',
                    'left': b'a',
                    'right': b'd',
                    'Up': b'W',
                    'Down': b'S',
                    'Left': b'A',
                    'Right': b'D',
                    'shoot': b' ',
                    'aim_up': b'q',
                    'aim_down': b'e',
                    'Aim_up': b'Q',
                    'Aim_down': b'E'
                },
                half='left'
            ),
            Player(
                x=900.0,  # Right side (75% of window width)
                y=100.0,
                color=[1.0, 0.0, 0.0],  # Red
                controls={
                    'up': b'i',
                    'down': b'k',
                    'left': b'j',
                    'right': b'l',
                    'Up': b'I',
                    'Down': b'K',
                    'Left': b'J',
                    'Right': b'L',
                    'shoot': b'\x01',  # Mouse Button 1 is handled separately
                    'aim_up': b'o',  # 'O' key
                    'aim_down': b'u',  # 'U' key
                    'Aim_up': b'O',
                    'Aim_down': b'U'
                },
                half='right'
            ),
        ]

        # Assign selected characters if provided
        if selected_characters_list:
            for idx, character in enumerate(selected_characters_list):
                players[idx].set_character(character)

        # Set Player2 as AI
        players[1].is_ai = True
        if not selected_characters["Player2"]:
            # Assign a random character if not already selected
            available_characters = ['Reety', 'Argha', 'Avishek']
            available_characters = [c for c in available_characters if c not in dead_characters]
            if available_characters:
                selected_ai_character = random.choice(available_characters)
                players[1].set_character(selected_ai_character)
                selected_characters["Player2"] = selected_ai_character
        else:
            players[1].set_character(selected_characters["Player2"])

    else:
        # Multiplayer Mode
        # Player1: Human Player on the Left
        # Player2: Human Player on the Right
        players = [
            Player(
                x=window_width / 4.0,  # Left side
                y=100.0,
                color=[0.0, 1.0, 0.0],  # Green
                controls={
                    'up': b'w',
                    'down': b's',
                    'left': b'a',
                    'right': b'd',
                    'Up': b'W',
                    'Down': b'S',
                    'Left': b'A',
                    'Right': b'D',
                    'shoot': b' ',
                    'aim_up': b'q',
                    'aim_down': b'e',
                    'Aim_up': b'Q',
                    'Aim_down': b'E'
                },
                half='left'
            ),
            Player(
                x=3 * window_width / 4.0,  # Right side
                y=100.0,
                color=[1.0, 0.0, 0.0],  # Red
                controls={
                    'up': b'i',
                    'down': b'k',
                    'left': b'j',
                    'right': b'l',
                    'Up': b'I',
                    'Down': b'K',
                    'Left': b'J',
                    'Right': b'L',
                    'shoot': b'\x01',  # Mouse Button 1 is handled separately
                    'aim_up': b'u',  # 'O' key
                    'aim_down': b'o',  # 'U' key
                    'Aim_up': b'U',
                    'Aim_down': b'O'
                },
                half='right'
            ),
        ]

        # Assign selected characters if provided
        if selected_characters_list:
            for idx, character in enumerate(selected_characters_list):
                players[idx].set_character(character)

        # Player2 remains a human player
        players[1].is_ai = False

def initialize_obstacles():
    """
    Initializes obstacles in the game environment.
    """
    global obstacles
    # obstacles = [
    #     Obstacle(x=300.0, y=200.0, width=150.0, height=20.0, color=(0.325, 0.478, 0.369)),
    #     Obstacle(x=600.0, y=400.0, width=200.0, height=20.0, color=(0.325, 0.478, 0.369)),
    #     Obstacle(x=400.0, y=600.0, width=180.0, height=20.0, color=(0.325, 0.478, 0.369)),
    #     Obstacle(x=500.0, y=0.0, width=50.0, height=200.0, color=(0.325, 0.478, 0.369))

    obstacles = [
    Obstacle(x=600.0, y=400.0, width=200.0, height=20.0, color=(0.325, 0.478, 0.369)),
    Obstacle(x=400.0, y=600.0, width=180.0, height=20.0, color=(0.325, 0.478, 0.369)),
    Obstacle(x=500.0, y=0.0, width=50.0, height=200.0, color=(0.369, 0.369, 0.369)),
    Obstacle(x=400.0, y=10.0, width=100.0, height=80.0, color=(0.722, 0.639, 0.541)),
    Obstacle(x=960.0, y=0.0, width=70.0, height=110.0, color=(0.369, 0.369, 0.369)),
    Obstacle(x=200.0, y=730.0, width=80.0, height=70.0, color=(0.722, 0.639, 0.541)),
        Obstacle(x=0.0, y=0.0, width=1200.0, height=30.0, color=(0.325, 0.478, 0.369))

        # Add more obstacles as needed
    ]

# ---------------------------
# 11. Collision Detection
# ---------------------------

def check_collisions():
    """
    Check for collisions between projectiles and players.
    Also, check for collisions between projectiles and obstacles.
    """
    global score, game_over_flags, game_state, current_round, dead_characters, coin_no
    for idx, shooter in enumerate(players):
        if shooter.game_over:
            continue
        for projectile in shooter.projectiles[:]:
            # Determine the target player
            target_idx = 1 - idx
            target = players[target_idx]
            if target.game_over:
                continue
            # Enhanced collision detection: check against entire stickman
            collision_radius = max(target.width, target.height) / 2.0 + 5.0  # Adjusted collision radius
            distance = math.hypot(projectile["x"] - target.x, projectile["y"] - target.y)
            if distance < collision_radius:
                # Hit detected
                if not target.shield_active:
                    target.health -= float(projectile["damage"])
                    print(f"Player {idx + 1} Hit Player {target_idx + 1}! Damage: {projectile['damage']} | Health Left: {int(target.health)}")
                    if target.health <= 0.0:
                        shooter.score += 1
                        print(f"Player {target_idx + 1} has been eliminated!")
                        game_over_flags[target_idx] = True
                        target.game_over = True
                        if not shooter.is_ai:
                            score[idx] += 1
                        # Mark the character as dead
                        dead_characters.add(target.selected_character_type.name)
                else:
                    print(f"Player {target_idx + 1} blocked the hit with Shield!")
                shooter.projectiles.remove(projectile)

                # Check if the round should end
                if any(game_over_flags):
                    if current_round < total_rounds:
                        # Prepare for next round
                        print(f"Round {current_round} ended. Preparing for next round...")
                        current_round += 1
                        reset_round()
                    else:
                        # End the game after the final round
                        determine_winner()
                break  # Prevent multiple collisions in the same frame

            #Check collision with obstacles and destroy bullet if collided
            for obstacle in obstacles:
                if obstacle.check_collision_with_point(projectile["x"], projectile["y"]):
                    print(f"Projectile collided with obstacle at ({projectile['x']}, {projectile['y']}). Destroying projectile.")
                    shooter.projectiles.remove(projectile)
                    break  # No need to check other obstacles

    # Check collision between players and coins
    for player in players:
        if player.game_over:
            continue
        for coin in coins[:]:
            distance_to_coin = math.hypot(player.x - coin.x, player.y - coin.y)
            if distance_to_coin < (player.width / 2.0 + coin.radius):
                # Collision detected: Player picks up the coin
                coin_no -= 1
                player.health += 5.0
                player.health = min(player.health, player.selected_character_type.health)  # Cap health at max
                print(f"{player.selected_character_type.name} picked up a coin! Health increased to {int(player.health)}")
                coins.remove(coin)

def reset_round():
    """
    Resets player positions and states for the next round.
    """
    global selected_characters, game_state
    for player in players:
        player.game_over = False
        player.health = float(player.selected_character_type.health)
        player.projectiles.clear()
        player.shield_active = False
        player.shield_end_time = 0.0
        # Reset to initial positions
        player.x = player.initial_x
        player.y = player.initial_y
    # Reset character selections for the next round
    # Characters that were dead remain dead and cannot be selected again
    selected_characters["Player1"] = None
    if not players[1].is_ai:
        selected_characters["Player2"] = None
    else:
        # AI retains its character unless it was dead
        if players[1].selected_character_type.name in dead_characters:
            # Assign a new character if available
            available_characters = ['Reety', 'Argha', 'Avishek']
            available_characters = [c for c in available_characters if c not in dead_characters]
            if available_characters:
                selected_ai_character = random.choice(available_characters)
                players[1].set_character(selected_ai_character)
                selected_characters["Player2"] = selected_ai_character
    # Transition to CharacterSelect for next round
    if game_state == "Singleplayer":
        game_state = "CharacterSelectSingle"
    else:
        game_state = "CharacterSelect"
    print(f"Starting Round {current_round} of {total_rounds}")

def determine_winner():
    """
    Determines the winner after all rounds are completed and transitions to the end screen.
    """
    global game_state
    if score[0] > score[1]:
        winner_text = "Congratulations Player 1!"
    elif score[1] > score[0]:
        winner_text = "Congratulations Player 2!"
    else:
        winner_text = "It's a Tie!"
    game_state = "Final"
    print("Game Over. Determining the winner...")
    print(winner_text)

def check_obstacle_collisions():
    """
    Prevent players from moving through obstacles.
    """

    for player in players:
        for obstacle in obstacles:
            # Simple AABB (Axis-Aligned Bounding Box) collision detection
            if (player.x + player.width / 2.0 > obstacle.x and
                    player.x - player.width / 2.0 < obstacle.x + obstacle.width and
                    player.y + player.height / 2.0 > obstacle.y and
                    player.y - player.height / 2.0 < obstacle.y + obstacle.height):
                # Collision detected; revert to previous position
                player.x = player.prev_x
                player.y = player.prev_y

# ---------------------------
# 12. Update Game State
# ---------------------------

def update_game(delta_time):
    """
    Update the game state, including player movements, projectile positions, and obstacle interactions.
    """
    global last_time, game_state, last_coin_spawn_time, coin_no
    if game_state not in ["Multiplayer", "Singleplayer"]:
        return

    current_time = time.time()

    #  Spawn coins at random intervals
    if current_time - last_coin_spawn_time >= coin_spawn_interval and coin_no < 10:
        coin_no+=1
        spawn_coin()
        last_coin_spawn_time = current_time

    # Update players
    for player in players:
        if not player.game_over:
            player.update(delta_time, current_time)

    # Check for collisions between projectiles and players (and obstacles)
    check_collisions()

    # Check for collisions between players and obstacles
    check_obstacle_collisions()

    last_time = current_time

#Spawn Coin Function
def spawn_coin():
    """
    Spawns a coin at a random position on the screen, avoiding obstacles.
    """
    max_attempts = 10
    for _ in range(max_attempts):
        x = random.uniform(20.0, window_width - 20.0)
        y = random.uniform(20.0, window_height - 20.0)
        # Ensure the coin does not spawn inside any obstacle
        collision = False
        for obstacle in obstacles:
            if obstacle.check_collision_with_point(x, y):
                collision = True
                break
        if not collision:
            coin = Coin(x, y)
            coins.append(coin)
            print(f"Spawned a coin at ({coin.x:.2f}, {coin.y:.2f})")
            break
    else:
        print("Failed to spawn a coin after maximum attempts.")

def reset_game():
    """
    Resets the entire game state for a new game.
    """
    global score, game_over_flags, current_round, dead_characters
    score = [0, 0]
    game_over_flags = [False, False]
    current_round = 1
    dead_characters = set()
    selected_characters["Player1"] = None
    selected_characters["Player2"] = None
    coins.clear()  # Clear all coins
    print("Game has been reset.")

# ---------------------------
# 13. Display Function
# ---------------------------

def display():
    """
    Render all game elements on the screen.
    """
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if game_state == "Main Menu":
        # Draw Main Menu background
        draw_rectangle(0.0, 0.0, window_width, window_height, (0.2, 0.2, 0.2))

        # Draw Main Menu title
        draw_main_menu_text()

        # Draw Main Menu buttons
        draw_buttons("Main Menu")

    elif game_state == "CharacterSelect":
        # Draw Character Select background
        draw_rectangle(0.0, 0.0, window_width, window_height, (0.2, 0.2, 0.2))

        # Draw Character Select title
        draw_character_select_text()

        # Draw Character Select buttons
        draw_buttons("CharacterSelect")

        # Draw selected characters
        draw_selected_characters()

    elif game_state == "CharacterSelectSingle":
        # Draw Character Select background
        draw_rectangle(0.0, 0.0, window_width, window_height, (0.2, 0.2, 0.2))

        # Draw Character Select title
        draw_character_select_text()

        # Draw Character Select buttons
        draw_buttons("CharacterSelectSingle")

        # Draw selected characters
        draw_selected_characters_single()

    elif game_state in ['Multiplayer', 'Singleplayer']:
        # Draw background
        glColor3f(0.627, 0.894, 1)  # Dark background
        glBegin(GL_QUADS)
        glVertex2f(0.0, 0.0)
        glVertex2f(float(window_width), 0.0)
        glVertex2f(float(window_width), float(window_height))
        glVertex2f(0.0, float(window_height))
        glEnd()

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw()

        #Draw coins
        for coin in coins:
            coin.draw()

        # Draw players and their projectiles
        for idx, player in enumerate(players):
            if not player.game_over:
                player.draw()
                for projectile in player.projectiles:
                    draw_ball(float(projectile["x"]), float(projectile["y"]), 5.0, [1.0, 1.0, 1.0])

                # Draw aiming line based on aim_angle
                aim_radians = math.radians(player.aim_angle)
                end_x = player.x + math.cos(aim_radians) * player.aim_line_length
                end_y = player.y + math.sin(aim_radians) * player.aim_line_length

                # Use aim_angle to determine target coordinates
                target_x, target_y = end_x, end_y
                draw_line_custom(player.x, player.y, target_x, target_y, player.color)

        # Draw gameplay UI elements
        draw_gameplay_ui()

    elif game_state == 'GameOver':
        # Draw Game Over background
        draw_rectangle(0.0, 0.0, window_width, window_height, (0.1, 0.0, 0.0))

        # Draw 'Game Over' text
        draw_game_over_text()

        # Display final scores
        glColor3f(1.0, 1.0, 1.0)  # White color
        glRasterPos2f(window_width / 2.0 - 80.0, window_height * 0.65)
        final_score_text = f"Final Scores - Player 1: {players[0].score} | Player 2: {players[1].score}"
        for char in final_score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        # Draw Game Over buttons
        draw_buttons("GameOver")

    elif game_state == 'Final':
        # Draw Final Screen background
        draw_rectangle(0.0, 0.0, window_width, window_height, (0.0, 0.0, 0.0))

        # Draw Congratulations or Tie text
        draw_game_over_text(winner_text="Congratulations!")

        # Display final scores
        glColor3f(1.0, 1.0, 1.0)  # White color
        glRasterPos2f(window_width / 2.0 - 80.0, window_height * 0.65)
        if score[0] > score[1]:
            final_score_text = f"Player 1 Wins with {score[0]} Points!"
        elif score[1] > score[0]:
            final_score_text = f"Player 2 Wins with {score[1]} Points!"
        else:
            final_score_text = f"It's a Tie! Both Players have {score[0]} Points."
        for char in final_score_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        # Draw Final Screen buttons
        draw_buttons("GameOver")

    # Swap buffers
    glutSwapBuffers()

# ---------------------------
# 14. Input Handlers
# ---------------------------

# (Already included above in section 9)

# ---------------------------
# 15. Timer Function
# ---------------------------

def timer(value):
    """
    Timer callback to update the game state and request redisplay.
    """
    current_time = time.time()
    delta_time = current_time - last_time
    update_game(delta_time)
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # Approximately 60 FPS

# ---------------------------
# 16. OpenGL Initialization
# ---------------------------

def init():
    """
    Initialize OpenGL settings.
    """
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glPointSize(2.0)  # Set point size for better visibility
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, window_width, 0.0, window_height)
    glMatrixMode(GL_MODELVIEW)

    # Enable blending for transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ---------------------------
# 17. Reshape Function
# ---------------------------

def reshape(width, height):
    """
    Handle window resizing for responsive design.
    """
    global window_width, window_height
    window_width = float(width)
    window_height = float(height)
    glViewport(0, 0, int(window_width), int(window_height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, window_width, 0.0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()

# ---------------------------
# 18. Main Function
# ---------------------------

def main():
    """
    Set up OpenGL, initialize the game, and start the main loop.
    """
    initialize_players()
    initialize_obstacles()

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(int(window_width), int(window_height))
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"JUDDHO - The War")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_keyboard_listener)
    glutKeyboardUpFunc(keyboard_key_up)
    glutMouseFunc(mouse_listener)
    glutPassiveMotionFunc(mouse_motion_callback)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

# ---------------------------
# 19. Entry Point
# ---------------------------

if __name__ == "__main__":
    main()