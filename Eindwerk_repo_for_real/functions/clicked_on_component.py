
from functions.cntrl_z_function import cntrl_z_function
from functions.Properties_menu import properties_menu


def clicked_on_component(dragged_comp, connections, components, mouse_pos, alt_button, timeline, copy_dragged_comp, zoom_factor, adding_comp, right_mouse_button):
    right_clicked_comp = None
    
    for comp in components:
        if comp.is_clicked(mouse_pos[0], mouse_pos[1]) and not dragged_comp and not right_mouse_button:            
            if not alt_button:   
                dragged_comp = comp
                components.remove(comp)
                cntrl_z_function(components, connections, timeline, zoom_factor, dragged_comp, data_2=None, action_type='clicked_component', undo_or_log='log')

            if alt_button:
                dragged_comp = comp.copy_with_same_id()
                copy_dragged_comp = True
                adding_comp = True
            break 
        elif comp.is_clicked(mouse_pos[0], mouse_pos[1]):
            right_clicked_comp = comp

    return dragged_comp, copy_dragged_comp, adding_comp, right_clicked_comp