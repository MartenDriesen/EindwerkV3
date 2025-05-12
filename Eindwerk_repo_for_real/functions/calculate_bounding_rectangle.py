import pygame
from main.global_constants import SPACING

def calculate_bounding_rectangle(selected_components, wires, camera_x, camera_y, zoom_factor):
    # Initialize min and max values
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    # Process components
    for comp in selected_components:   
        min_x = min(min_x, comp.x)
        min_y = min(min_y, comp.y)
        if comp.rotation == 90 or comp.rotation == 270:
            size_x = comp.size_y
            size_y = comp.size_x
            max_x = max(max_x, comp.x + size_x)
            max_y = max(max_y, comp.y + size_y)
        else:
            max_x = max(max_x, comp.x + comp.size_x)
            max_y = max(max_y, comp.y + comp.size_y)


    # Process wires
    for wire in wires:
        start_x, start_y = wire.start_pos
        end_x, end_y = wire.end_pos
        min_x = min(min_x, start_x, end_x)
        min_y = min(min_y, start_y, end_y)
        max_x = max(max_x, start_x, end_x)
        max_y = max(max_y, start_y, end_y)

    # Calculate rectangle
    x = min_x
    y = min_y
    width = max_x - min_x
    height = max_y - min_y

    rect_x = (((x) // SPACING) * (SPACING + zoom_factor)) - camera_x
    rect_y = (((y) // SPACING) * (SPACING + zoom_factor)) - camera_y
    rect_width = ((width) // SPACING) * (SPACING + zoom_factor)
    rect_height = ((height) // SPACING) * (SPACING + zoom_factor)
    
    rect = pygame.rect.Rect(x, y, width, height)
    
    if selected_components or wires:
        return (rect_x, rect_y, rect_width, rect_height), rect
    else:
        return None, None
    
    
