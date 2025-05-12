import pygame
from main.global_constants import RED, BLACK

def check_component_collision(component, components, lines):
    """
    Check if the dragged component collides with any existing lines.
    If a collision is detected, the component turns red.

    :param component: The currently dragged component.
    :param lines: List of existing lines as tuples ((x1, y1), (x2, y2)).
    :return: Boolean indicating collision status.
    """

    rect_dragged_comp = pygame.Rect(component.x, component.y, component.size_x, component.size_y)
    adjusted_rect = rect_dragged_comp.inflate(-2, -2)

    for line in lines:
        start= line.start_pos
        end = line.end_pos
        # Check if the line intersects with the component's bounding box
        if adjusted_rect.clipline(start, end):
            # Change the component's image to red
            component.color = RED
            return True
        
    for comp in components:
            rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
            rect = rect.inflate(-2, -2)
            if rect.colliderect(adjusted_rect):
                return True   

    # Reset to the original image if no collision is detected
    component.color = BLACK
    return False