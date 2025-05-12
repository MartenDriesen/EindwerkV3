from main.global_constants import SPACING
from functions.snap_to_grid import snap_to_grid

def replace_selected_components_and_connections(adding_comp, dragged_comp, raw_offsets_dragged_comp_x, raw_offsets_dragged_comp_y, camera_x, camera_y, selected_components, selected_wires, selected_comps_wires, raw_offsets_comp, raw_offsets_line, mouse_pos, zoom_factor, continious_left_mouse_button, copy_dragged_comp, virtual_selecting_box, pasted):
    virtual_mouse_pos_plus_camera = (((mouse_pos[0] + camera_x) / (SPACING + zoom_factor)) * SPACING), (((mouse_pos[1] + camera_y) / (SPACING + zoom_factor)) * SPACING)   
    comp_offset_x, comp_offset_y = snap_to_grid(virtual_mouse_pos_plus_camera[0], virtual_mouse_pos_plus_camera[1])

    if (continious_left_mouse_button or pasted) and selected_comps_wires and not virtual_selecting_box and (raw_offsets_comp or raw_offsets_line):        
        for i, comp in enumerate(selected_components, start=0):
            x = comp_offset_x - raw_offsets_comp[i][0] 
            y = comp_offset_y - raw_offsets_comp[i][1]
            comp.x = x
            comp.y = y
            comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
            comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING)

        for i, line in enumerate(selected_wires, start=0):  
            start = comp_offset_x - raw_offsets_line[i][0][0], comp_offset_y - raw_offsets_line[i][0][1]
            end = comp_offset_x - raw_offsets_line[i][1][0], comp_offset_y - raw_offsets_line[i][1][1]
            line.start_pos = start
            line.end_pos = end
            start = (SPACING + zoom_factor) * (start[0] / SPACING), (SPACING + zoom_factor) * (start[1] / SPACING)
            end = (SPACING + zoom_factor) * (end[0] / SPACING), (SPACING + zoom_factor) * (end[1] / SPACING)
            line.virtual_start_pos = start
            line.virtual_end_pos = end

    elif dragged_comp and not adding_comp:  
        x = comp_offset_x - raw_offsets_dragged_comp_x 
        y = comp_offset_y - raw_offsets_dragged_comp_y
        dragged_comp.x = x
        dragged_comp.y = y   
        dragged_comp.virtual_x = (SPACING + zoom_factor) * (dragged_comp.x / SPACING)
        dragged_comp.virtual_y = (SPACING + zoom_factor) * (dragged_comp.y / SPACING) 
    
    elif (dragged_comp and adding_comp and not copy_dragged_comp) or (dragged_comp and adding_comp and copy_dragged_comp and continious_left_mouse_button): 
        dragged_comp.x = comp_offset_x - raw_offsets_dragged_comp_x
        dragged_comp.y = comp_offset_y - raw_offsets_dragged_comp_y
        dragged_comp.virtual_x = (SPACING + zoom_factor) * (dragged_comp.x / SPACING)
        dragged_comp.virtual_y = (SPACING + zoom_factor) * (dragged_comp.y / SPACING)