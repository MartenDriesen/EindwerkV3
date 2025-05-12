import pygame
from functions.component_data_pins_and_hotzones import component_pinout_with_hotzones
from main.global_constants import screen, BLACK, SPACING

def is_mouse_in_hotzone(component, virtual_mouse_pos_x , virtual_mouse_pos_y, camera_x, camera_y, zoom_factor):
    # Get the component's rotated image and its bounding rect
    image =  pygame.transform.scale(pygame.image.load(component.image_path), (component.size_x, component.size_y))
    rotated_image = pygame.transform.rotate(image, component.rotation)
    component_rect = rotated_image.get_rect(topleft=(component.x, component.y))
    
    # Get the current hotzones for this component at its current rotation
    component_name = type(component).__name__  # e.g., "Resistor"

       # Iterate over the dictionary keys (tuples)
    for key_tuple, pinout_data in component_pinout_with_hotzones.items():
        if component_name in key_tuple:
            component_data = pinout_data
            break
    hotzones = component_data.get(component.rotation, [])
    pin_pos = None
    # Iterate over the hotzones
    for hotzone in hotzones:
        zone = hotzone["zone"]
        # Check if the mouse position is inside the zone by comparing coordinates
        # This is assuming that the zone is a rectangle in the image coordinates

        if zone[0][0] <= virtual_mouse_pos_x - component_rect.x <= zone[0][1] and zone[1][0] <= virtual_mouse_pos_y - component_rect.y <= zone[1][1]:
            # Draw a black circle at the 'pin' position relative to the component's image
            pin_pos = (hotzone["pin"][0] + component.x, hotzone["pin"][1] + component.y)
            pin_pos_to_draw = (hotzone["pin"][0] + component.x, hotzone["pin"][1] + component.y)
            pin_pos_to_draw = ((pin_pos_to_draw[0] / SPACING) * (SPACING + zoom_factor)) - camera_x, ((pin_pos_to_draw[1] / SPACING) * (SPACING + zoom_factor)) - camera_y
            pygame.draw.circle(screen, BLACK, pin_pos_to_draw, 5)
            return pin_pos
    return pin_pos