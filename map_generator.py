import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Map Generator")

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

# Current block type being placed
current_block = SLINGSHOT

# Grid
rows = HEIGHT // GRID_SIZE
cols = WIDTH // GRID_SIZE
grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

# Create "maps" folder if it doesn't exist
os.makedirs("maps", exist_ok=True)


def draw_grid():
    """Draw the grid lines and blocks."""
    screen.fill(WHITE)

    # Draw grid lines
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw blocks
    for row in range(rows):
        for col in range(cols):
            block_type = grid[row][col]
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if block_type == SLINGSHOT:
                pygame.draw.rect(screen, RED, rect)
            elif block_type == ICE_BLUE_BLOCK:
                pygame.draw.rect(screen, ICE_BLUE, rect)
            elif block_type == BROWN_BLOCK:
                pygame.draw.rect(screen, BROWN, rect)


def save_map(map_name):
    """Save the grid to a file."""
    file_path = os.path.join("maps", f"{map_name}.json")
    with open(file_path, "w") as f:
        json.dump(grid, f)
    print(f"Map saved to {file_path}")


def get_grid_pos(mouse_pos):
    """Convert mouse position to grid position."""
    x, y = mouse_pos
    return y // GRID_SIZE, x // GRID_SIZE


def text_input_box():
    """Display a text input box to get the map name."""
    font = pygame.font.SysFont(None, 36)
    input_active = True
    user_text = ""

    while input_active:
        screen.fill(WHITE)
        prompt = font.render("Enter map name: ", True, BLACK)
        input_box = pygame.Rect(200, HEIGHT // 2, 400, 50)
        pygame.draw.rect(screen, GRAY, input_box, 2)

        # Render user text
        user_text_surface = font.render(user_text, True, BLACK)
        screen.blit(prompt, (200, HEIGHT // 2 - 40))
        screen.blit(user_text_surface, (input_box.x + 10, input_box.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    return user_text


def main():
    global current_block

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_block = SLINGSHOT
                elif event.key == pygame.K_2:
                    current_block = ICE_BLUE_BLOCK
                elif event.key == pygame.K_3:
                    current_block = BROWN_BLOCK
                elif event.key == pygame.K_s:
                    map_name = text_input_box()
                    save_map(map_name)
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to place block
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    grid[row][col] = current_block
                elif event.button == 3:  # Right click to remove block
                    row, col = get_grid_pos(pygame.mouse.get_pos())
                    grid[row][col] = EMPTY

        draw_grid()

        # Display instructions
        font = pygame.font.SysFont(None, 24)
        instructions = [
            "1: Place Slingshot (Red)",
            "2: Place Ice-Blue Block (Breakable)",
            "3: Place Brown Block (Indestructible)",
            "Left Click: Place Block",
            "Right Click: Remove Block",
            "S: Save Map",
        ]
        for i, text in enumerate(instructions):
            label = font.render(text, True, BLACK)
            screen.blit(label, (10, HEIGHT - 120 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
