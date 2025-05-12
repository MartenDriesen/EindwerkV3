import pygame
from main.global_constants import ORANGE, SELECTEDCOMP
from functions.is_mouse_near_line import is_mouse_near_line

def draw_existing_connections(connections, selected_wires, camera_x, camera_y, continious_left_mouse_button, virtual_mouse_pos):
    for line in connections:

        if line in selected_wires and not continious_left_mouse_button:
            connections.remove(line)    

        near_line, closest_point = is_mouse_near_line(virtual_mouse_pos, line, threshold=5)

      
        color = line.color     
        if line in selected_wires:
           color = SELECTEDCOMP                  
        
        line.draw(color, camera_x, camera_y)