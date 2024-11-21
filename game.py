import pygame
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Cubes Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
ICE_BLUE = (173, 216, 230)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Block types
EMPTY = 0
SLINGSHOT = 1
ICE_BLUE_BLOCK = 2
BROWN_BLOCK = 3


class Cube:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.vel_x = 0
        self.vel_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Gravity
        self.vel_y += 0.5

        # Prevent going out of bounds
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.vel_y = 0


def draw_grid(grid):
    """Draw the game grid with blocks."""
    for row_idx, row in enumerate(grid):
        for col_idx, block in enumerate(row):
            rect = pygame.Rect(col_idx * GRID_SIZE, row_idx * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if block == SLINGSHOT:
                pygame.draw.rect(screen, RED, rect)
            elif block == ICE_BLUE_BLOCK:
                pygame.draw.rect(screen, ICE_BLUE, rect)
            elif block == BROWN_BLOCK:
                pygame.draw.rect(screen, BROWN, rect)


def load_map(map_name):
    """Load the map from the maps folder."""
    with open(f"maps/{map_name}.json", "r") as f:
        return json.load(f)


def game_loop(grid):
    """Main game loop."""
    clock = pygame.time.Clock()
    running = True
    sling_point = None
    for row_idx, row in enumerate(grid):
        for col_idx, block in enumerate(row):
            if block == SLINGSHOT:
                sling_point = (col_idx * GRID_SIZE + GRID_SIZE // 2, row_idx * GRID_SIZE + GRID_SIZE // 2)
                break
        if sling_point:
            break

    cubes = []
    current_cube = None
    mouse_dragging = False

    while running:
        screen.fill(WHITE)

        # Draw the game elements
        draw_grid(grid)

        # Draw sling point
        if sling_point:
            pygame.draw.circle(screen, RED, sling_point, 10)

        # Draw cubes
        for cube in cubes:
            cube.move()
            cube.draw(screen)

        # Sling line
        if mouse_dragging and current_cube:
            pygame.draw.line(screen, BLACK, sling_point, pygame.mouse.get_pos(), 2)

        pygame.display.flip()
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if sling_point and not current_cube:
                    mouse_dragging = True
                    current_cube = Cube(sling_point[0] - 20, sling_point[1] - 20, 20, GRAY)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Release sling
                if mouse_dragging and current_cube:
                    mouse_dragging = False
                    # Calculate velocity based on mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = sling_point[0] - mouse_x
                    dy = sling_point[1] - mouse_y
                    current_cube.vel_x = dx / 10
                    current_cube.vel_y = dy / 10
                    cubes.append(current_cube)
                    current_cube = None


if __name__ == "__main__":
    map_name = input("Enter map name to load: ")
    grid = load_map(map_name)
    game_loop(grid)
