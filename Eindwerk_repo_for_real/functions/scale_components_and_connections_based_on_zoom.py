from main.global_constants import SPACING

def scale_components_and_connections_based_on_zoom(components, connections, selected_components, selected_wires, dragged_comp, zoom_factor):
   
    for comp in components:
        scale_x = (SPACING + zoom_factor) * (comp.size_x / SPACING)
        scale_y = (SPACING + zoom_factor) * (comp.size_y / SPACING)
        comp.scale_x = (SPACING + zoom_factor) * (scale_x / (SPACING + zoom_factor)) 
        comp.scale_y = (SPACING + zoom_factor) * (scale_y / (SPACING + zoom_factor))
        comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
        comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING)

    for comp in selected_components:
        scale_x = (SPACING + zoom_factor) * (comp.size_x / SPACING)
        scale_y = (SPACING + zoom_factor) * (comp.size_y / SPACING)
        comp.scale_x = (SPACING + zoom_factor) * (scale_x / (SPACING + zoom_factor)) 
        comp.scale_y = (SPACING + zoom_factor) * (scale_y / (SPACING + zoom_factor)) 
        comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
        comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING)    

    if dragged_comp:
        scale_x = (SPACING + zoom_factor) * (dragged_comp.size_x / SPACING)
        scale_y = (SPACING + zoom_factor) * (dragged_comp.size_y / SPACING)
        dragged_comp.scale_x = (SPACING + zoom_factor) * (scale_x / (SPACING + zoom_factor)) 
        dragged_comp.scale_y = (SPACING + zoom_factor) * (scale_y / (SPACING + zoom_factor)) 
        dragged_comp.virtual_x = (SPACING + zoom_factor) * (dragged_comp.x / SPACING)
        dragged_comp.virtual_y = (SPACING + zoom_factor) * (dragged_comp.y / SPACING)

    for conn in connections:    
        start = (SPACING + zoom_factor) * (conn.start_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.start_pos[1] / SPACING)
        end = (SPACING + zoom_factor) * (conn.end_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.end_pos[1] / SPACING)
        conn.virtual_start_pos = start
        conn.virtual_end_pos = end

    for conn in selected_wires:    
        start = (SPACING + zoom_factor) * (conn.start_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.start_pos[1] / SPACING)
        end = (SPACING + zoom_factor) * (conn.end_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.end_pos[1] / SPACING)
        conn.virtual_start_pos = start
        conn.virtual_end_pos = end    