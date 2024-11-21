import pygame
import math
from config import GRAVITY, DRAG

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slingshot Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CUBE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

# Cube class
class Cube:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = 20
        self.color = color
        self.vx = 0
        self.vy = 0
        self.launched = False

    def update(self):
        if self.launched:
            self.vy += GRAVITY  # Apply gravity
            self.vx *= DRAG     # Apply drag
            self.vy *= DRAG     # Apply drag
            self.x += self.vx
            self.y += self.vy

            # Bounce off walls
            if self.x < 0 or self.x + self.size > WIDTH:
                self.vx = -self.vx
                self.x = max(0, min(self.x, WIDTH - self.size))
            # Bounce off floor/ceiling
            if self.y < 0 or self.y + self.size > HEIGHT:
                self.vy = -self.vy
                self.y = max(0, min(self.y, HEIGHT - self.size))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Slingshot mechanic
def calculate_trajectory(start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    return -dx / 5, -dy / 5  # Adjust scaling factor as needed

# Main game loop
def main():
    clock = pygame.time.Clock()
    running = True

    # Initial settings
    cube = Cube(200, HEIGHT - 100, CUBE_COLORS[0])
    cubes = []
    slingshot_anchor = (200, HEIGHT - 100)
    dragging = False

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not cube.launched:
                dragging = True
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                cube.vx, cube.vy = calculate_trajectory(slingshot_anchor, pygame.mouse.get_pos())
                cube.launched = True
                cubes.append(cube)
                # Spawn a new cube
                cube = Cube(200, HEIGHT - 100, CUBE_COLORS[len(cubes) % len(CUBE_COLORS)])

        # Update cube position
        for c in cubes:
            c.update()

        # Draw slingshot line
        if dragging:
            pygame.draw.line(screen, BLACK, slingshot_anchor, pygame.mouse.get_pos(), 2)

        # Draw cubes
        for c in cubes:
            c.draw(screen)
        cube.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
