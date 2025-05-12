import pygame
from main.global_constants import RED, SELECTEDCOMP
from functions.check_line_overlap import check_line_overlap

def draw_selected_components_and_connections(components, connections, selected_components, selected_wires, camera_x, camera_y, start_pos_selecting_rect):
    comp_is_colliding = False 
    line_is_colliding = False
    if not start_pos_selecting_rect:
        for comp in selected_components:

            rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
  
            for component in components:
                component_rect = pygame.Rect(component.x, component.y, component.size_x, component.size_y)
                if rect.colliderect(component_rect) and not comp_is_colliding:
                    comp_is_colliding = True
                    break 
        for comp in selected_components:
            rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
            adjusted_rect = rect.inflate(-2, -2)
            for line in connections:
                if adjusted_rect.clipline(line.start_pos, line.end_pos) and not comp_is_colliding:
                    comp_is_colliding = True
                    break                    
   
        for line in selected_wires:
            for comp in components:
                rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
                adjusted_rect = rect.inflate(-2, -2)
                if adjusted_rect.clipline(line.start_pos, line.end_pos):
                   line_is_colliding = True
                   break
        for line in selected_wires:
                if check_line_overlap(line.start_pos, line.end_pos, connections):
                   line_is_colliding = True             
     
    for comp in selected_components: 
        if comp_is_colliding or line_is_colliding:
           comp.color = RED 
        else:
            comp.color = SELECTEDCOMP   
               
        comp.draw(camera_x, camera_y) 
   
    for line in selected_wires:
        if comp_is_colliding or line_is_colliding:
            color = RED 
        else:
            color = SELECTEDCOMP
       
        line.draw(color, camera_x, camera_y)

    return comp_is_colliding, line_is_colliding        


