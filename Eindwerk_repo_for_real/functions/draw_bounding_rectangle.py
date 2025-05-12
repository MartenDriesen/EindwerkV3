import pygame
from main.global_constants import screen

def draw_bounding_rectangle(bounding_rectangle, color=(1, 153, 255), alpha=40):
    """
    Draws a partly transparent rectangle on the screen.

    Parameters:
    - bounding_rectangle: Tuple (x, y, width, height) representing the rectangle.
    - color: RGB tuple for the rectangle color (default is red).
    - alpha: Transparency level (0 = fully transparent, 255 = fully opaque).
    """
    # Unpack rectangle dimensions
    x, y, width, height = bounding_rectangle

    # Create a transparent surface
    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Fill the surface with the color and alpha
    transparent_surface.fill((*color, alpha))  # Add alpha to the color tuple

    # Blit the transparent surface onto the screen
    screen.blit(transparent_surface, (x, y))
