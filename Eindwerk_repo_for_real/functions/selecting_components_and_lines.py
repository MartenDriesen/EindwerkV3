import pygame
from main.global_constants import SELECTEDCOMP
from functions.cntrl_z_function import cntrl_z_function

def selecting_components_and_lines(virtual_selecting_box, selected_components, selected_wires, components, connections, ctrl_button, a_button, timeline, zoom_factor):

    if virtual_selecting_box:
        selected_components.clear()
        selected_wires.clear()

    for comp in components:
        rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
        if virtual_selecting_box:
            if virtual_selecting_box.colliderect(rect):
                comp.color = SELECTEDCOMP
                selected_components.append(comp)            
           
    for line in connections:
        if virtual_selecting_box:
            if virtual_selecting_box.clipline(line.start_pos, line.end_pos):
                selected_wires.append(line)           

    if ctrl_button and a_button and not selected_components and not selected_wires:    
        selected_components.extend(components) 
        selected_wires.extend(connections) 
        cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='selected_components_and_connections', undo_or_log='log')        