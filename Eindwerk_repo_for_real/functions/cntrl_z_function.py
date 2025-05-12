import copy
from main.global_constants import SPACING
from functions.update_pin_positions_on_grid import update_pin_positions_on_grid

relative_pos = None
relative_comp_pos = None
relative_conn_pos = None
timeline_cntrl_shift_z = []

def cntrl_z_function(components, connections, timeline, zoom_factor, data, data_2, action_type, undo_or_log, max_actions=40):

    global relative_pos, relative_comp_pos, relative_conn_pos, timeline_cntrl_shift_z

    if action_type == 'clicked_component':
        relative_comp = copy.deepcopy(data)
        relative_pos = relative_comp.x, relative_comp.y, relative_comp.rotation
        return

    if action_type == 'selected_components_and_connections':  
        relative_comps = copy.deepcopy(data)
        relative_conns = copy.deepcopy(data_2)
        relative_comp_pos = [(comp.x, comp.y, comp.rotation, comp.id) for comp in relative_comps]
        relative_conn_pos = [(conn.start_pos, conn.end_pos, conn.id) for conn in relative_conns]
        return

    if undo_or_log == 'log' and action_type:
        timeline_cntrl_shift_z.clear()
        if len(timeline) >= max_actions:
            timeline.pop(0)

        if action_type == 'added_component':        
            timeline.append({'action': action_type, 'data': data.id})
            return

        if action_type == 'added_connection':       
            timeline.append({'action': action_type, 'data': data.id})
            return

        if action_type == 'removed_component':        
            timeline.append({'action': action_type, 'data': (data.copy_with_same_id())})
            return

        if action_type == 'added_components_and_connections':
            components_ids = []
            connections_ids = []
            components_ids = [comp.id for comp in data]
            connections_ids = [conn.id for conn in data_2]
            timeline.append({'action': action_type, 'data': (components_ids.copy(), connections_ids.copy())}) 
            return
        
        if action_type == 'removed_components_and_connections':
            timeline.append({'action': action_type, 'data': (copy.deepcopy(data), copy.deepcopy(data_2))})
            return
               
        if action_type == 'replaced_component': 
            if data.x != relative_pos[0] or data.y != relative_pos[1] or data.rotation != relative_pos[2]:
                timeline.append({'action': action_type, 'data': (data.id, relative_pos)})
                relative_comp = None
                return

        if action_type == 'replaced_components_and_connections':
            components_ids = []
            connections_ids = []
            components_ids = [comp.id for comp in data]
            connections_ids = [conn.id for conn in data_2]    
            if relative_comp_pos: 
                first_tuple = next(iter(relative_comp_pos))   
          
                if ((data[0].x != first_tuple[0] or data[0].y != first_tuple[1] or data[0].rotation != first_tuple[2]) and relative_comp_pos):          
                    timeline.append({'action': action_type, 'data': (components_ids, connections_ids, relative_comp_pos.copy(), relative_conn_pos.copy())})
                    return
            elif relative_conn_pos:
                first_tuple_2 = next(iter(relative_conn_pos)) 

                if ((data_2[0].start_pos != first_tuple_2[0] or data_2[0].end_pos != first_tuple_2[1]) and relative_conn_pos):             
                    timeline.append({'action': action_type, 'data': (components_ids, connections_ids, relative_comp_pos.copy(), relative_conn_pos.copy())})
                    return

    elif undo_or_log == 'undo':
        if not timeline:
            return

        last_action = timeline.pop()
        action_type = last_action['action']
        value = last_action['data']

        if action_type == 'added_component':    
           
            for comp in components:
                if value == comp.id:
                    components.remove(comp)
                    timeline_cntrl_shift_z.append({'action': 'removed_component', 'data': comp})
                    break
 
        elif action_type == 'added_connection':  

            for conn in connections:
                if value == conn.id:
                    connections.remove(conn)
                    timeline_cntrl_shift_z.append({'action': 'removed_connection', 'data': conn})
                    break

        elif action_type == 'removed_component':

            components.append(value)       
            timeline_cntrl_shift_z.append({'action': 'added_removed_component', 'data': (value.id)})        

        elif action_type == 'added_components_and_connections':

            components_ids, connections_ids = value
        
            removed_components = []  # To store removed components
            removed_connections = []  # To store removed connections
            
            for id in components_ids:
                for comp in components:
                    if id == comp.id:
                        components.remove(comp)
                        removed_components.append(comp)
                        break
        
            for id in connections_ids:
                for conn in connections:
                    if id == conn.id:
                        connections.remove(conn)
                        removed_connections.append(conn)


            timeline_cntrl_shift_z.append({'action': 'removed_added_components_and_connections', 'data': (copy.deepcopy(removed_components), copy.deepcopy(removed_connections))})  

        elif action_type == 'removed_components_and_connections': 
 
            removed_components, removed_connections = value
            
            components_ids = [comp.id for comp in removed_components]  # Use a set directly
            connections_ids = [conn.id for conn in removed_connections]


            components.extend(removed_components)        
            connections.extend(removed_connections)          

            timeline_cntrl_shift_z.append({'action': 'added_removed_components_and_connections', 'data': (components_ids.copy(), connections_ids.copy())})          

        elif action_type == 'replaced_component':
           
            id, old_comp = value
            
            for comp in components:
                if comp.id == id:
                    relative_pos_2 = comp.x, comp.y, comp.rotation
                    comp.x = old_comp[0] # Restore position
                    comp.y = old_comp[1] # Restore position
                    comp.rotation = old_comp[2]
                    comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
                    comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING) 
                    update_pin_positions_on_grid(comp)
                    timeline_cntrl_shift_z.append({'action': 'replace_replaced_component', 'data': (id, relative_pos_2)})
                    break
    
        elif action_type == 'replaced_components_and_connections':

            components_ids, connections_ids, old_component_positions, old_connection_positions = value

            old_component_positions = list(old_component_positions)
            old_connection_positions = list(old_connection_positions)

            relative_comp_2 = []
            relative_conn_2 = []

            for i, id in enumerate(components_ids, start=0):
                for comp in components:
                    if comp.id == id:
                        relative_comp_2.append((comp.x, comp.y, comp.rotation))
                        comp.x = old_component_positions[i][0] # Restore position
                        comp.y = old_component_positions[i][1] # Restore position
                        comp.rotation = old_component_positions[i][2]
                        comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
                        comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING) 
                        update_pin_positions_on_grid(comp)
                        break

            for i, id in enumerate(connections_ids, start=0):                  
                for conn in connections:
                    if id == conn.id:
                        relative_conn_2.append((conn.start_pos, conn.end_pos))
                        conn.start_pos = old_connection_positions[i][0] # Restore position
                        conn.end_pos = old_connection_positions[i][1] # Restore position
                        start = (SPACING + zoom_factor) * (conn.start_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.start_pos[1] / SPACING)
                        end = (SPACING + zoom_factor) * (conn.end_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.end_pos[1] / SPACING)
                        conn.virtual_start_pos = start
                        conn.virtual_end_pos = end
                        break

            timeline_cntrl_shift_z.append({'action': 'replace_replaced_components_and_connections', 'data': (components_ids.copy(), connections_ids.copy(), relative_comp_2.copy(), relative_conn_2.copy())})

    elif undo_or_log == 'undo_undo':
        if not timeline_cntrl_shift_z:
            return

        last_action = timeline_cntrl_shift_z.pop()
        action_type = last_action['action']
        value = last_action['data']

        if action_type == 'removed_component':        
                components.append(value)
                timeline.append({'action': 'added_component', 'data': value.id})
 
        elif action_type == 'removed_connection':        
                connections.append(value)
                timeline.append({'action': 'added_connection', 'data': value.id})

        elif action_type == 'added_removed_component':
            for comp in components:
                if value == comp.id:
                    components.remove(comp)
                    timeline.append({'action': 'removed_component', 'data': comp})
                    break     

        elif action_type == 'removed_added_components_and_connections':
            removed_components, removed_connections = value
            components_ids = []
            connections_ids = []
            components_ids = [comp.id for comp in removed_components]
            connections_ids = [conn.id for conn in removed_connections]


            components.extend(removed_components)        
            connections.extend(removed_connections)          

            timeline.append({'action': 'added_components_and_connections', 'data': (components_ids.copy(), connections_ids.copy())})   

        elif action_type == 'added_removed_components_and_connections':
            components_ids, connections_ids = value
        
            removed_components = []  # To store removed components
            removed_connections = []  # To store removed connections
            
            for id in components_ids:
                for comp in components:
                    if id == comp.id:
                        components.remove(comp)  
                        removed_components.append(comp)
                        break

            for id in connections_ids:
                for conn in connections:
                    if id == conn.id:
                        connections.remove(conn)
                        removed_connections.append(conn)
                        break        

            timeline.append({'action': 'removed_components_and_connections', 'data': (copy.deepcopy(removed_components), copy.deepcopy(removed_connections))})   
                     

        elif action_type == 'replace_replaced_component':

            id, old_comp = value

            for comp in components:
                if comp.id == id:
                    relative_pos_3 = comp.x, comp.y, comp.rotation
                    comp.x = old_comp[0] # Restore position
                    comp.y = old_comp[1] # Restore position
                    comp.rotation = old_comp[2]
                    comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
                    comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING) 
                    update_pin_positions_on_grid(comp)
                    timeline.append({'action': 'replaced_component', 'data': (id, relative_pos_3)})
                    break
    
        elif action_type == 'replace_replaced_components_and_connections':
            components_ids, connections_ids, old_component_positions, old_connection_positions = value

            old_component_positions = list(old_component_positions)
            old_connection_positions = list(old_connection_positions)

            relative_comp_2 = []
            relative_conn_2 = []

            for i, id in enumerate(components_ids, start=0):
                for comp in components:
                    if comp.id == id:
                        relative_comp_2.append((comp.x, comp.y, comp.rotation))
                        comp.x = old_component_positions[i][0] # Restore position
                        comp.y = old_component_positions[i][1] # Restore position
                        comp.rotation = old_component_positions[i][2]
                        comp.virtual_x = (SPACING + zoom_factor) * (comp.x / SPACING)
                        comp.virtual_y = (SPACING + zoom_factor) * (comp.y / SPACING) 
                        update_pin_positions_on_grid(comp)
                        break

            for i, id in enumerate(connections_ids, start=0):                  
                for conn in connections:
                    if id == conn.id:
                        relative_conn_2.append((conn.start_pos, conn.end_pos))
                        conn.start_pos = old_connection_positions[i][0] # Restore position
                        conn.end_pos = old_connection_positions[i][1] # Restore position
                        start = (SPACING + zoom_factor) * (conn.start_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.start_pos[1] / SPACING)
                        end = (SPACING + zoom_factor) * (conn.end_pos[0] / SPACING), (SPACING + zoom_factor) * (conn.end_pos[1] / SPACING)
                        conn.virtual_start_pos = start
                        conn.virtual_end_pos = end
                        break

            timeline.append({'action': 'replaced_components_and_connections', 'data': (components_ids.copy(), connections_ids.copy(), relative_comp_2.copy(), relative_conn_2.copy())})