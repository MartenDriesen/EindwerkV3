import pygame
from main.global_constants import SPACING, LIGHT_GRAY, SCREEN_WIDTH, SCREEN_HEIGHT  # Importing constants

def draw_virtual_grid(screen, camera_x, camera_y, zoom_factor):
    """Draw the virtual grid relative to the camera offset."""
    # Start drawing the grid from the top-left corner of the screen
    spacing = SPACING + zoom_factor
    for x in range(-camera_x % spacing, SCREEN_WIDTH, spacing):
        pygame.draw.line(screen, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(-camera_y % spacing, SCREEN_HEIGHT, spacing):
        pygame.draw.line(screen, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))
