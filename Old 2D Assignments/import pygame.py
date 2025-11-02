import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AMBER = (255, 191, 0)

# Circle properties
CIRCLE_RADIUS = 20
FALL_SPEED = 3

# Spaceship properties
SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 10
SPACESHIP_SPEED = 5

# Game states
running = True
game_over = False

# Pygame screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot the Circles!")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Spaceship class
class Spaceship:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
        self.width = SPACESHIP_WIDTH
        self.height = SPACESHIP_HEIGHT
        self.color = GREEN

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= SPACESHIP_SPEED
        elif direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += SPACESHIP_SPEED

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Circle class
class Circle:
    def __init__(self):
        self.x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
        self.y = 0
        self.radius = CIRCLE_RADIUS
        self.color = RED
        self.speed = FALL_SPEED

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Projectile class
class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.color = BLUE
        self.speed = -8

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Collision detection
def is_collision(circle, projectile):
    distance = math.sqrt((circle.x - projectile.x) ** 2 + (circle.y - projectile.y) ** 2)
    return distance < circle.radius + projectile.radius

# Game initialization
spaceship = Spaceship()
falling_circles = []
projectiles = []
scores = 0
missed_circles = 0

# Main game loop
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        spaceship.move("left")
    if keys[pygame.K_d]:
        spaceship.move("right")
    if keys[pygame.K_SPACE]:
        if len(projectiles) < 5:  # Limit the number of projectiles
            projectiles.append(Projectile(spaceship.x + spaceship.width // 2, spaceship.y))

    # Update falling circles
    if random.randint(1, 50) == 1:  # Spawn new circle occasionally
        falling_circles.append(Circle())

    for circle in falling_circles[:]:
        circle.move()
        if circle.y > SCREEN_HEIGHT:
            falling_circles.remove(circle)
            missed_circles += 1
            if missed_circles >= 3:
                game_over = True

    # Update projectiles
    for projectile in projectiles[:]:
        projectile.move()
        if projectile.y < 0:
            projectiles.remove(projectile)

    # Check for collisions
    for circle in falling_circles[:]:
        for projectile in projectiles[:]:
            if is_collision(circle, projectile):
                falling_circles.remove(circle)
                projectiles.remove(projectile)
                scores += 1

    # Draw objects
    spaceship.draw()
    for circle in falling_circles:
        circle.draw()
    for projectile in projectiles:
        projectile.draw()

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {scores}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Check game over
    if game_over:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
