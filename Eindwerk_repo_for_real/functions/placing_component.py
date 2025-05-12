import copy
from functions.update_pin_positions_on_grid import update_pin_positions_on_grid
from functions.cntrl_z_function import cntrl_z_function
from functions.update_component_name import update_component_name

is_copy = False
dragged_is_copy = ''

def placing_component(dragged_component, selected_components, selected_wires, selected_comps_wires, comp_is_colliding, selected_comps_colliding, selected_lines_colliding, adding_comp, components, connections, timeline, copy_dragged_comp, zoom_factor, left_mouse_button_place_comp, continious_left_mouse_button, alt_button, left_mouse_button, pasted, esc_button, cntrl_v):
  
    global is_copy, dragged_is_copy

    placed_comp = False
    placed_components = False

    if (dragged_component and not comp_is_colliding and (left_mouse_button_place_comp or esc_button) and not adding_comp) or (dragged_component and adding_comp and not comp_is_colliding and not copy_dragged_comp and (left_mouse_button_place_comp or esc_button)) or (dragged_component and adding_comp and not comp_is_colliding and copy_dragged_comp and not pasted and not continious_left_mouse_button) or (dragged_component and not comp_is_colliding and cntrl_v):
 
        if dragged_is_copy == '' and cntrl_v:
            dragged_is_copy = 'first placing'

        if (not adding_comp or copy_dragged_comp or cntrl_v) and dragged_is_copy != 'first placing' and not left_mouse_button:
            comp_to_append = dragged_component.copy_with_new_id()
            print('new_id')
        else:
            comp_to_append = dragged_component

        comp_to_append.needs_update = True    

        # Place the dragged component
        update_pin_positions_on_grid(comp_to_append)
        components.append(comp_to_append)    

        if (adding_comp and left_mouse_button) or copy_dragged_comp or cntrl_v:
            if dragged_is_copy == 'first copy' or adding_comp or copy_dragged_comp:
                cntrl_z_function(components, connections, timeline, zoom_factor, comp_to_append, data_2=None, action_type='added_component', undo_or_log='log')
                print('added')
                update_component_name(components, comp_to_append, var=False)
            else:
                cntrl_z_function(components, connections, timeline, zoom_factor, comp_to_append, data_2=None, action_type='replaced_component', undo_or_log='log')    
                dragged_is_copy = 'first copy'
                print('replaced')
        else:
            cntrl_z_function(components, connections, timeline, zoom_factor, comp_to_append, data_2=None, action_type='replaced_component', undo_or_log='log')    
            dragged_is_copy = ''
            print('replaced')

        copy_dragged_comp = False
        placed_comp = True

    elif selected_comps_wires and not selected_comps_colliding and not selected_lines_colliding and (left_mouse_button_place_comp or (alt_button and left_mouse_button) or cntrl_v or (pasted and left_mouse_button) or esc_button):
        
        temporary = []
        temporary_2 = []
                
        for comp in selected_components: 
            # Place the dragged component
            comp.needs_update = True 
            update_pin_positions_on_grid(comp)
            components.append(comp)
            if alt_button:
                temporary.append(comp.copy_with_new_id())
            
        for conn in selected_wires:
            # Place the dragged wires
            conn.needs_update = True    
            connections.append(conn) 
            if alt_button:
                temporary_2.append(conn.copy_with_new_id())   

        if (is_copy and not alt_button and left_mouse_button_place_comp and not cntrl_v) or (alt_button and not left_mouse_button_place_comp and is_copy and not cntrl_v) or (pasted and left_mouse_button):
            cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='added_components_and_connections', undo_or_log='log') 
            update_component_name(components, dragged_component, var = True)
            if (is_copy or pasted) and left_mouse_button_place_comp:
                is_copy = False 
            else:
                is_copy = True    
 
        elif (alt_button and left_mouse_button and not is_copy) or (left_mouse_button_place_comp and not is_copy):          
            cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='replaced_components_and_connections', undo_or_log='log')
            if alt_button and left_mouse_button and not is_copy:
                is_copy = True 
        selected_components.clear()
        selected_wires.clear()

        if is_copy:
            selected_components.extend(copy.deepcopy(temporary))
            selected_wires.extend(copy.deepcopy(temporary_2))

        placed_components = True    
    
    return copy_dragged_comp, placed_comp, placed_components

