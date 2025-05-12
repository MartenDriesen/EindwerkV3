import pygame
import uuid
import copy
from main.global_constants import screen, BLACK, screen_rect
from functions.get_non_transparent_area_dragged_comp import get_non_transparent_area_dragged_comp

class Component:
    def __init__(self, image_path, size_x, size_y):
        self.id = uuid.uuid4()
        self.image_path = image_path
        self.x = 0
        self.y = 0
        self.virtual_x = 0
        self.virtual_y = 0
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = size_x
        self.scale_y = size_y
        self.rotation = 0
        self.color = BLACK
        self.edited = False

    def draw_properties(self, zoom_factor, camera_x, camera_y):

        if not hasattr(self, "properties"):
            return
        fontsize = 18
        font = pygame.font.Font(None, fontsize) 
        
        if zoom_factor > 0:
            font = pygame.font.Font(None, fontsize + zoom_factor)       


        if zoom_factor > -3:

            if hasattr(self, "properties"):
                property_value = self.properties[0][1]
                property_name = self.properties[0][0]
                text_name = font.render(f"{property_value} {property_name}", True, BLACK)
                text_rect = self.virtual_x + self.scale_x - camera_x, self.virtual_y - camera_y  # Get dimensions of the text
                screen.blit(text_name, text_rect)
                if hasattr(self, "name"):
                    comp_name =  font.render(f"{self.name}", True, BLACK) 
                    comp_rect = self.virtual_x + self.scale_x - camera_x, self.virtual_y - camera_y - fontsize 
                    screen.blit(comp_name, comp_rect)
                
                # Blit the text onto the screen
                
    def draw(self, camera_x, camera_y):
        # Rotate the image around the top-left corner
        image = pygame.transform.scale(pygame.image.load(self.image_path), (self.scale_x, self.scale_y))
        rotated_image = pygame.transform.rotate(image, self.rotation)

        # Get the new rotated rectangle's bounds
        rect = rotated_image.get_rect(topleft=(self.x, self.y))  # Corrected
        rect_w, rect_h = rect.width, rect.height  # Access width and height from the Rect

        # Get the non-transparent area with the desired color
        image_to_display = get_non_transparent_area_dragged_comp(rotated_image, rect_w, rect_h, self.color)
        
        x, y = self.virtual_x - camera_x, self.virtual_y - camera_y
        rect = pygame.rect.Rect(x, y, self.scale_x, self.scale_y)
        # Blit the final image onto the surface
        if rect.colliderect(screen_rect):
            screen.blit(image_to_display, (x, y))


    def rotate(self):
        self.rotation = (self.rotation - 90) % 360

    def is_clicked(self, mouse_x, mouse_y):
        # Check if the mouse is inside the rotated component's bounding box
        rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        return rect.collidepoint(mouse_x, mouse_y)

    def get_non_transparent_area(self, comp_color):
        """
        Returns a surface with only non-transparent pixels turned to the specified color.

        Args:
        comp_color: A tuple representing the color (R, G, B, A) to apply.
        """
        # Extract the alpha channel as a NumPy array
        image =  pygame.transform.scale(pygame.image.load(self.image_path), (self.scale_x, self.scale_y))
        alpha = pygame.surfarray.pixels_alpha(image)

        # Create a new surface with the same size and alpha channel
        color_image = pygame.Surface(self.scale_x, self.scale_y, flags=pygame.SRCALPHA)

        # Fill the new surface with the desired color
        color_image.fill(comp_color)

        # Set the alpha of transparent areas to 0
        color_array = pygame.surfarray.pixels_alpha(color_image)
        color_array[alpha == 0] = 0  # Keep transparent areas fully transparent
    
        return color_image
    
   # Fully independent copy with the same ID
    def copy_with_same_id(self):
        new_instance = copy.deepcopy(self)  # Create a fully independent copy
        new_instance.id = self.id  # Retain the same ID
        return new_instance

    # Fully independent copy with a new ID
    def copy_with_new_id(self):
        new_instance = copy.deepcopy(self)  # Create a fully independent copy
        new_instance.id = uuid.uuid4()  # Assign a new unique ID
        return new_instance

        
        