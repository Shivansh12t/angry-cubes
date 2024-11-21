import pygame
import os
import json

from game import game_loop, load_map


pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


def list_maps():
    """List all available maps in the maps folder."""
    maps_folder = "maps"
    return [f.split(".json")[0] for f in os.listdir(maps_folder) if f.endswith(".json")]


def display_map_selection():
    """Show the available maps and let the user select one."""
    font = pygame.font.SysFont(None, 36)
    maps = list_maps()
    selected_map = None

    while not selected_map:
        screen.fill(WHITE)
        title = font.render("Select a map:", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, map_name in enumerate(maps):
            map_text = font.render(f"{i + 1}. {map_name}", True, BLACK)
            screen.blit(map_text, (100, 150 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_1, pygame.K_1 + len(maps)):
                    selected_map = maps[event.key - pygame.K_1]

    return selected_map


def main_menu():
    """Display the opening screen."""
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        screen.fill(WHITE)
        title = font.render("Main Menu", True, BLACK)
        option1 = small_font.render("1. Load Map", True, BLACK)
        option2 = small_font.render("2. Create Map", True, BLACK)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, 200))
        screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_map = display_map_selection()
                    if selected_map:
                        grid = load_map(selected_map)
                        game_loop(grid)
                        print(f"Playing map: {selected_map}")  # Replace with game logic
                elif event.key == pygame.K_2:
                    os.system("python map_generator.py")


if __name__ == "__main__":
    main_menu()
