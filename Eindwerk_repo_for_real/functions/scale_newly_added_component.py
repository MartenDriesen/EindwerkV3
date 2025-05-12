from main.global_constants import SPACING

def scale_newly_added_component(dragged_component, zoom_factor):
        
    scale_x = (SPACING + zoom_factor) * (dragged_component.size_x / SPACING)
    scale_y = (SPACING + zoom_factor) * (dragged_component.size_y / SPACING)
    dragged_component.scale_x = (SPACING + zoom_factor) * (scale_x / (SPACING + zoom_factor)) 
    dragged_component.scale_y = (SPACING + zoom_factor) * (scale_y / (SPACING + zoom_factor)) 
