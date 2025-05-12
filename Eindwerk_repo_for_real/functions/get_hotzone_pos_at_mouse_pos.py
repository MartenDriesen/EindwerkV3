import pygame
from main.global_constants import screen, BLACK, SPACING
from functions.snap_to_grid import snap_to_grid, snap_to_virtual_grid

def get_and_draw_hotzone_pos_at_mouse_pos(virtual_mouse_pos, camera_x, camera_y, zoom_factor):
    closest_point_on_grid = None
    closest_point_on_virtual_grid = None
    remember_hotzone_pos = None
    mouse_in_hotzone = False
                
    closest_point_on_grid = snap_to_grid(virtual_mouse_pos[0], virtual_mouse_pos[1]) 
    remember_hotzone_pos = closest_point_on_grid
    closest_point_2 = (closest_point_on_grid[0] / SPACING) * (SPACING + zoom_factor), (closest_point_on_grid[1] / SPACING) * (SPACING + zoom_factor)
    closest_point_on_virtual_grid = snap_to_virtual_grid(closest_point_2[0], closest_point_2[1], zoom_factor)
    mouse_in_hotzone = True

    # Draw a black circle
    closest_point_on_grid_to_draw = closest_point_on_virtual_grid[0] - camera_x, closest_point_on_virtual_grid[1] - camera_y
    pygame.draw.circle(screen, BLACK, closest_point_on_grid_to_draw, 5)        

    return remember_hotzone_pos, mouse_in_hotzone