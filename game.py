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
YELLOW = (255, 255, 0)  # BirdCube color

# Block types
EMPTY = 0
SLINGSHOT = 1
ICE_BLUE_BLOCK = 2
BROWN_BLOCK = 3


class BirdCube:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.collision_slowdown = 0.7  # Default velocity reduction

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
            self.vel_y = -self.vel_y * 0.5  # Bounce back with reduced velocity

    def check_collision(self, grid):
        """Check for collision with blocks and apply block-specific effects."""
        row = self.rect.y // GRID_SIZE
        col = self.rect.x // GRID_SIZE

        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            block_type = grid[row][col]
            if block_type == ICE_BLUE_BLOCK:
                grid[row][col] = EMPTY  # Break the block
                self.vel_x *= self.collision_slowdown  # Reduce speed
                self.vel_y *= self.collision_slowdown
            elif block_type == BROWN_BLOCK:
                # Axis-based collision detection
                block_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)

                if self.rect.colliderect(block_rect):
                    # Calculate penetration depth
                    overlap_x = min(block_rect.right - self.rect.left, self.rect.right - block_rect.left)
                    overlap_y = min(block_rect.bottom - self.rect.top, self.rect.bottom - block_rect.top)

                    if overlap_x < overlap_y:  # Horizontal collision
                        if self.rect.centerx < block_rect.centerx:
                            self.rect.right = block_rect.left  # Left side
                            self.vel_x = -abs(self.vel_x) * 0.8
                        else:
                            self.rect.left = block_rect.right  # Right side
                            self.vel_x = abs(self.vel_x) * 0.8
                    else:  # Vertical collision
                        if self.rect.centery < block_rect.centery:
                            self.rect.bottom = block_rect.top  # Top side
                            self.vel_y = -abs(self.vel_y) * 0.8
                        else:
                            self.rect.top = block_rect.bottom  # Bottom side
                            self.vel_y = abs(self.vel_y) * 0.8


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

    bird_cube = None
    cubes = []  # Track launched cubes
    mouse_dragging = False

    while running:
        screen.fill(WHITE)

        # Draw the game elements
        draw_grid(grid)

        # Draw sling point
        if sling_point:
            pygame.draw.circle(screen, RED, sling_point, 10)

        # Draw bird cubes
        for cube in cubes:
            cube.move()
            cube.check_collision(grid)
            cube.draw(screen)

        # Draw the active bird cube being dragged
        if mouse_dragging and bird_cube:
            bird_cube.rect.center = pygame.mouse.get_pos()
            bird_cube.draw(screen)
            pygame.draw.line(screen, BLACK, sling_point, bird_cube.rect.center, 2)

        pygame.display.flip()
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if sling_point and not bird_cube:
                    # Create a new bird cube at the sling point
                    mouse_dragging = True
                    bird_cube = BirdCube(sling_point[0] - 10, sling_point[1] - 10, 20, YELLOW)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Release sling
                if mouse_dragging and bird_cube:
                    mouse_dragging = False
                    # Calculate velocity based on sling displacement
                    dx = sling_point[0] - bird_cube.rect.centerx
                    dy = sling_point[1] - bird_cube.rect.centery
                    bird_cube.vel_x = dx / 10
                    bird_cube.vel_y = dy / 10
                    cubes.append(bird_cube)  # Add to launched cubes
                    bird_cube = None



if __name__ == "__main__":
    map_name = input("Enter map name to load: ")
    grid = load_map(map_name)
    game_loop(grid)
