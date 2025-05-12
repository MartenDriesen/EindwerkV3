import pygame

def get_non_transparent_area_dragged_comp(image, scale_x, scale_y, color):
        """
        Returns a surface with only non-transparent pixels turned to the specified color.

        Args:
        comp_color: A tuple representing the color (R, G, B, A) to apply.
        """
        # Extract the alpha channel as a NumPy array
        alpha = pygame.surfarray.pixels_alpha(image)

        # Create a new surface with the same size and alpha channel
        color_image = pygame.Surface((scale_x, scale_y), flags=pygame.SRCALPHA)

        # Fill the new surface with the desired color
        color_image.fill(color)

        # Set the alpha of transparent areas to 0
        color_array = pygame.surfarray.pixels_alpha(color_image)
        color_array[alpha == 0] = 0  # Keep transparent areas fully transparent
    
        return color_image