from functions.snap_to_grid import snap_to_grid
from main.global_constants import SPACING

def rotate_component_connections(dragged_component, selected_comps_wires, selected_components, selected_wires, zoom_factor, bounding_rect, raw_offsets_comp, raw_offsets_line):
    if dragged_component:
        dragged_component.rotate() 
    if selected_comps_wires:
        raw_offsets_comp.clear()
        raw_offsets_line.clear()
        rotation_point = bounding_rect.center
        x, y = snap_to_grid(rotation_point[0], rotation_point[1])
        for comp in selected_components:
            offset_x = comp.x - x
            offset_y = comp.y - y
            rotated_x = -offset_y 
            rotated_y = offset_x
            comp.x = rotated_x + x
            comp.y = rotated_y + y
            # Rotate the image around its top-left corner
            comp.rotate()
            if comp.rotation == 90:
                comp.x -= comp.size_x
            if comp.rotation == 180:
                comp.x -= comp.size_x
            if comp.rotation == 270:
                comp.x -= comp.size_x
            if comp.rotation == 0:
                comp.x -= comp.size_x
            offset = x - comp.x, y - comp.y
            raw_offsets_comp.append(offset)      
            comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
            comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING)   
                              
        for line in selected_wires:
            # Extract start and end positions
            start_x, start_y = line.start_pos
            end_x, end_y = line.end_pos
            # Calculate offsets relative to the mouse position for the start position
            offset_start_x = start_x - x
            offset_start_y = start_y - y
            # Rotate start position around the mouse (90-degree rotation)
            rotated_start_x = -offset_start_y
            rotated_start_y = offset_start_x
            # Update start position
            line.start_pos = (rotated_start_x + x, rotated_start_y + y)
            # Calculate offsets relative to the mouse position for the end position
            offset_end_x = end_x - x
            offset_end_y = end_y - y
            # Rotate end position around the mouse (90-degree rotation)
            rotated_end_x = -offset_end_y
            rotated_end_y = offset_end_x
            # Update end position
            line.end_pos = (rotated_end_x + x, rotated_end_y + y)
            start_offset = (x - line.start_pos[0], y - line.start_pos[1])
            end_offset = (x - line.end_pos[0], y - line.end_pos[1])
            raw_offsets_line.append((start_offset, end_offset)) 
            start = line.start_pos
            end = line.end_pos
            start = (SPACING + zoom_factor) * (start[0] / SPACING), (SPACING + zoom_factor) * (start[1] / SPACING)
            end = (SPACING + zoom_factor) * (end[0] / SPACING), (SPACING + zoom_factor) * (end[1] / SPACING)
            line.virtual_start_pos = start
            line.virtual_end_pos = end

 