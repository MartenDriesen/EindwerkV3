import pygame
from main.global_constants import ORANGE, SELECTEDCOMP, BLACK

def draw_existing_components(components, selected_components, virtual_mouse_pos, dragged_component, selected_comps_wires, drawing_line, camera_x, camera_y, continious_left_mouse_button, zoom_factor):

    hovering_over_comp = False

    for comp in components:
        if comp.rotation in [90, 270]:
            rect = pygame.Rect(comp.x, comp.y, comp.size_y, comp.size_x)
        else:
            rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)    
        if rect.collidepoint(virtual_mouse_pos):
           if not dragged_component and not selected_comps_wires and not drawing_line:
              comp.color = SELECTEDCOMP
              hovering_over_comp = True
        elif not comp in selected_components:   
            comp.color = BLACK
        if comp in selected_components and not continious_left_mouse_button:
            components.remove(comp)             
        comp.draw(camera_x, camera_y) 
        comp.draw_properties(zoom_factor, camera_x, camera_y)

    return hovering_over_comp    