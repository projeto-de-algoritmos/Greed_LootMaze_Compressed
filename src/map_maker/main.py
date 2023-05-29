import pygame
import sys

# Define constants for the screen width and height
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800

# Define constants for the different colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# Define a constant for the cell size
CELL_SIZE = 20

# Define a list of palette colors
PALETTE = [COLOR_WHITE, COLOR_BLACK, COLOR_GREEN, COLOR_BLUE]

# Create a 2D array to represent the map
map_grid = [[COLOR_WHITE for _ in range(SCREEN_HEIGHT // CELL_SIZE - 1)] for _ in range(SCREEN_WIDTH // CELL_SIZE)]

# Set the initially selected color
selected_color = COLOR_WHITE

# Define the Save button
SAVE_BUTTON = pygame.Rect(SCREEN_WIDTH - CELL_SIZE * 4, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE * 4, CELL_SIZE)


def draw_map(screen, map_grid):
    for i, row in enumerate(map_grid):
        for j, color in enumerate(row):
            pygame.draw.rect(screen, color, pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_palette(screen):
    for i, color in enumerate(PALETTE):
        pygame.draw.rect(screen, color, pygame.Rect(i * CELL_SIZE * 2, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE * 2, CELL_SIZE))

def draw_button(screen, button, text):
    pygame.draw.rect(screen, COLOR_BLACK, button)
    font = pygame.font.Font(None, 24)
    label = font.render(text, True, COLOR_WHITE)
    screen.blit(label, (button.x + 5, button.y + 5))

def save_map(map_grid):
    image = Image.new('RGBA', (len(map_grid), len(map_grid[0])))
    pixels = image.load()

    for i, row in enumerate(map_grid):
        for j, color in enumerate(row):
            pixels[i, j] = color

    image.save('map.png')

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    global selected_color

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If the user presses the mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse
                x, y = pygame.mouse.get_pos()

                # If the user clicked on the palette
                if y >= SCREEN_HEIGHT - CELL_SIZE:
                    # If the user clicked on the Save button
                    if SAVE_BUTTON.collidepoint(x, y):
                        save_map(map_grid)
                    else:
                        selected_color = PALETTE[x // (CELL_SIZE * 2)]
                else:
                    # Change the color of the cell that the user clicked on
                    map_grid[x // CELL_SIZE][y // CELL_SIZE] = selected_color


        # Check if the mouse button is currently being pressed
        if pygame.mouse.get_pressed()[0]:
            # Get the position of the mouse
            x, y = pygame.mouse.get_pos()

            # If the mouse is not over the palette
            if y < SCREEN_HEIGHT - CELL_SIZE:
                # Change the color of the cell that the mouse is over
                map_grid[x // CELL_SIZE][y // CELL_SIZE] = selected_color

        # Draw the map
        draw_map(screen, map_grid)

        # Draw the color palette
        draw_palette(screen)

        # Draw the save button
        draw_button(screen, SAVE_BUTTON, "SAVE")


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
