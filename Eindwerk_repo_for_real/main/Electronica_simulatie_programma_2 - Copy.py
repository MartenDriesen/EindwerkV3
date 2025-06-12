import pygame
import sys
import numpy as np

# Dynamically add the project directory to the Python module search path
project_path = r"C:/Users/marte/Documents/eindwerk/EindwerkV3/Eindwerk_repo_for_real"
if project_path not in sys.path:
    sys.path.append(project_path)

from main.global_constants import *

from functions.logo import logo

from functions.manual import open_manual
from functions.manage_classes_button import manage_classes_button, upload_feedback
from functions.login import draw_login_register_menu, logout, show_user
from functions.draw_virtual_grid import draw_virtual_grid
from functions.componentMenus import componentMenus, save_component
from functions.hide_component_menu import hide_component_menu
from functions.feedback import get_feedback
from functions.draw_Ui_and_UI_user_input import draw_Ui, select_connection_color
from functions.placing_component import placing_component
from functions.snap_to_grid import snap_to_grid, snap_to_virtual_grid
from functions.check_comp_collision import check_component_collision
from functions.get_hotzone_pos_at_mouse_pos import get_and_draw_hotzone_pos_at_mouse_pos
from functions.rotate_component_connections import rotate_component_connections
from functions.replace_selected_components_and_connections import replace_selected_components_and_connections
from functions.create_and_draw_selecting_box import create_and_draw_selecting_box
from functions.selecting_components_and_lines import selecting_components_and_lines
from functions.draw_existing_components import draw_existing_components
from functions.draw_selected_components_and_connections import draw_selected_components_and_connections
from functions.draw_existing_connections import draw_existing_connections
from functions.clicked_on_component import clicked_on_component
from functions.draw_collision_circles import draw_collision_circles
from functions.save_load_projects import save_button, newFile, show_project_name, load_project, new_file_button, is_menu_open, save_as_button, load_mongo_file
from functions.scale_components_and_connections_based_on_zoom import scale_components_and_connections_based_on_zoom
from functions.scale_newly_added_component import scale_newly_added_component
from functions.cntrl_z_function import cntrl_z_function, timeline_cntrl_shift_z
from functions.calculate_bounding_rectangle import calculate_bounding_rectangle
from functions.draw_bounding_rectangle import draw_bounding_rectangle
from functions.Properties_menu import properties_menu, is_property_menu_open
from functions.import_project import import_project
from functions.update_component_name import update_component_name
from functions.shortcuts import shortcuts

from component_classes.Component import Component
from component_classes.subConnection import subConnection

from component_classes.Connection import Connection
from component_classes.AC_Motor import AC_Motor
from component_classes.DC_Motor import DC_Motor
from component_classes.Capacitor import Capacitor
from component_classes.Current_Meter import Current_Meter
from component_classes.AC_Voltage_Src import AC_Voltage_Src
from component_classes.DC_Voltage_Src import DC_Voltage_Src
from component_classes.Diode import Diode
from component_classes.Fuse import Fuse
from component_classes.IGBT_N_Channel import IGBT_N_Channel
from component_classes.IGBT_P_Channel import IGBT_P_Channel
from component_classes.Inductor import Inductor
from component_classes.JFET_N_Channel import JFET_N_Channel
from component_classes.JFET_P_Channel_ import JFET_P_Channel
from component_classes.LDR import LDR
from component_classes.LED import LED
from component_classes.MOSFET_N_Depl import MOSFET_N_Depl
from component_classes.MOSFET_N_Enhance import MOSFET_N_Enhance
from component_classes.MOSFET_P_Depl import MOSFET_P_Depl
from component_classes.MOSFET_P_Enhance import MOSFET_P_Enhance
from component_classes.Normally_Open_Switch import Normally_Open_Switch
from component_classes.Normally_Closed_Switch import Normally_Closed_Switch
from component_classes.NPN_Transistor import NPN_Transistor
from component_classes.PNP_Transistor import PNP_Transistor
from component_classes.Polar_Capacitor import Polar_Capacitor
from component_classes.Potentiometer import Potentiometer
from component_classes.Battery import Battery
from component_classes.Normally_Open_Relay import Normally_Open_Relay
from component_classes.Normally_Closed_Relay import Normally_Closed_Relay
from component_classes.Resistor import Resistor
from component_classes.Schottky_Diode import Schottky_Diode
from component_classes.SCR import SCR
from component_classes.Thermistor import Thermistor
from component_classes.Transformer import Transformer
from component_classes.Triac import Triac
from component_classes.Var_Capacitor import Var_Capacitor
from component_classes.Var_Inductor import Var_Inductor
from component_classes.Var_Polar_Capacitor import Var_Polar_Capacitor
from component_classes.Varistor import Varistor
from component_classes.Volt_Meter import Volt_Meter
from component_classes.Power_Meter import Power_Meter
from component_classes.Zener_Diode import Zener_Diode
from component_classes.Three_Phase_Motor_Delta import Three_Phase_Motor_Delta
from component_classes.Three_Phase_Motor_Star import Three_Phase_Motor_Star
from component_classes.Three_Phase_Power_Src import Three_Phase_Power_Src
from component_classes.Ground import Ground
from component_classes.Photo_Diode import Photo_Diode
from component_classes.Ohm_Meter import Ohm_Meter

from component_classes.Teleruptor import Teleruptor
from component_classes.Three_Way_Switch import Three_Way_Switch
from component_classes.Four_Way_Switch import Four_Way_Switch
from component_classes.SPS_Open import SPS_Open
from component_classes.DPST import DPST
from component_classes.DPST_Open import DPST_Open
from component_classes.SPST import SPST
from component_classes.TPST_Open import TPST_Open
from component_classes.Staircase_Timer_Auto import Staircase_Timer_Auto
from component_classes.Circuit_Breaker import Circuit_Breaker
from component_classes.feedbackBlock import feedbackBlock
from component_classes.Socket import Socket
from component_classes.Lamp import Lamp

components = []
connections = []
selected_components = []
selected_wires = []
copied_components = []
copied_wires = []
raw_offsets_comp = []
raw_offsets_line = []
timeline = []

userdetails = None
user_id = None
wasFeedbackBlock = None
feedbackBlockBool = None
saved_comp = None
clicked_icon = None
start_pos_selecting_rect = None
end_pos_selecting_rect = None
key_down_event = None
dragged_component = None
virtual_selecting_box = None
loaded_components = None
loaded_connections = None

imported_components = None
imported_connections = None
comp_name = None
mouse_pos_dragged_comp = None
bounding_rectangle = None
bounding_rectangle_meassurements = None
copied_component = None
saved_component = None
edit_component_props = None
right_clicked_comp = None
logged_user = None

is_teacher = None
class_menu_open = False
menu_is_open = False
placed_comp_is_saved_comp = False
left_mouse_button = False
continious_left_mouse_button = False
right_mouse_button = False
shift_button = False
ctrl_button = False
z_button = False
y_button = False
a_button = False
c_button = False
v_button = False
m_button = False
alt_button = False
esc_button = False
cntrl_v = False
hide_menu = False
mouse_in_ui = False 
comp_is_colliding = False
drawing_line = False
line_is_colliding = False
selected_comps_wires = False
adding_component = False
mouse_in_hotzone = False
user_input_temp_bool = False
user_input_light_bool = False 
copy_dragged_comp = False
left_mouse_button_place_comp = False
selected_comps_colliding = False
selected_lines_colliding = False
pasted = False
placed_comp = False
menu_is_open_check = False
property_menu_is_open = False
hovering_over_comp = False
hand_cursor = False
loggedout = False

zoom_factor = 0
camera_offset_x = 0
camera_offset_y = 0
drag_offset_x = 0
drag_offset_y = 0
raw_offsets_dragged_comp = 0, 0
env_temp = 21
env_light = 1000
selectingbox_timer = 120

current_line = subConnection()

# Main loop
running = True
while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    start_menu_is_open = is_menu_open()
    property_menu_is_open = is_property_menu_open()

    if start_menu_is_open or property_menu_is_open:
        menu_is_open = True
        remember_hotzone_pos = None
        mouse_in_hotzone = False
    else:
        menu_is_open = False

    virtual_mouse_pos = (((mouse_pos[0] + camera_offset_x) / (SPACING + zoom_factor)) * SPACING), (((mouse_pos[1] + camera_offset_y) / (SPACING + zoom_factor)) * SPACING)
    
    if ((mouse_pos[0] < new_width2 or mouse_pos[1] < new_height) and not hide_menu) or (hide_menu and mouse_pos[1] < new_height): #is mouse in ui
        mouse_in_ui = True
    else:
        mouse_in_ui = False 
    if len(selected_components) > 0 or len(selected_wires) > 0:
        selected_comps_wires = True  
        mouse_in_hotzone = False
        remember_hotzone_pos = None 
    else:     
        selected_comps_wires = False 
    
    if shift_button and continious_left_mouse_button:
        dragging_camera = True 
    else:
        dragging_camera = False         
   
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                            

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click 
                Click_time = pygame.time.get_ticks()  # Record the current time 
                left_mouse_button = True    
                continious_left_mouse_button = True  
                end_pos_selecting_rect = None 
                mouse_pos_dragged_comp = snap_to_grid(virtual_mouse_pos[0], virtual_mouse_pos[1])
                if bounding_rectangle:
                    if selected_comps_wires and (not bounding_rectangle.collidepoint(virtual_mouse_pos) or pasted) and not shift_button and not selected_lines_colliding and not selected_comps_colliding and not mouse_in_ui:
                        left_mouse_button_place_comp = True 
                if dragged_component and not shift_button and not comp_is_colliding and not line_is_colliding and not mouse_in_ui:
                        left_mouse_button_place_comp = True    
                              
                if selected_comps_wires and not shift_button and not virtual_selecting_box:
                    raw_offsets_comp.clear()
                    raw_offsets_line.clear()
                    end_pos_selecting_rect = snap_to_grid(virtual_mouse_pos[0], virtual_mouse_pos[1]) 
                    for comp in selected_components:
                        offset = end_pos_selecting_rect[0] - comp.x, end_pos_selecting_rect[1] - comp.y
                        raw_offsets_comp.append(offset)  
                    for wire in selected_wires:
                        start_offset = (end_pos_selecting_rect[0] - wire.start_pos[0], end_pos_selecting_rect[1] - wire.start_pos[1])
                        end_offset = (end_pos_selecting_rect[0] - wire.end_pos[0], end_pos_selecting_rect[1] - wire.end_pos[1])
                        raw_offsets_line.append((start_offset, end_offset)) 

                if bounding_rectangle:        
                    if not bounding_rectangle.collidepoint(virtual_mouse_pos):
                        start_pos_selecting_rect = virtual_mouse_pos
                if not selected_comps_wires and not dragged_component:
                    start_pos_selecting_rect = virtual_mouse_pos        
                 
            elif event.button == 3:  # Right click
                drawing_line = False
                mouse_in_hotzone = False  
                current_line = subConnection()  # Reset the line    
                right_mouse_button = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click released
                left_mouse_button_up = True
                continious_left_mouse_button = False 
                Click_time = pygame.time.get_ticks() - Click_time                                              
                start_pos_selecting_rect = None
                virtual_selecting_box = None  
                if selected_comps_wires and not bounding_rectangle:
                    cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='selected_components_and_connections', undo_or_log='log')            
            #if event.button == 3:
                
                    
        elif event.type == pygame.MOUSEMOTION: 
            if dragging_camera:    
                # Update camera offset based on mouse movement
                dx, dy = event.rel
                camera_offset_x -= dx
                camera_offset_y -= dy 
                if selected_comps_wires:
                    bounding_rectangle_meassurements, bounding_rectangle = calculate_bounding_rectangle(selected_components, selected_wires, camera_offset_x, camera_offset_y, zoom_factor)   

        elif event.type == pygame.MOUSEWHEEL:

            if ctrl_button and not menu_is_open:
                old_zoom_factor = zoom_factor
                if event.y > 0:  # Scroll up
                    zoom_factor += ZOOMSENSITIVITY
                    zoom_factor = max(MINZOOM, min(MAXZOOM, zoom_factor))
                elif event.y < 0:  # Scroll down
                    zoom_factor -= ZOOMSENSITIVITY
                    zoom_factor = max(MINZOOM, min(MAXZOOM, zoom_factor))  

                old_spacing = SPACING + old_zoom_factor
                new_spacing = SPACING + zoom_factor
                camera_offset_x += (mouse_pos[0] + camera_offset_x) / old_spacing * (new_spacing - old_spacing)
                camera_offset_y += (mouse_pos[1] + camera_offset_y) / old_spacing * (new_spacing - old_spacing)
                camera_offset_x = int(camera_offset_x)
                camera_offset_y = int(camera_offset_y)     
                scale_components_and_connections_based_on_zoom(components, connections, selected_components, selected_wires, dragged_component, zoom_factor)
                if selected_comps_wires:
                    bounding_rectangle_meassurements, bounding_rectangle = calculate_bounding_rectangle(selected_components, selected_wires, camera_offset_x, camera_offset_y, zoom_factor) 


        elif event.type == pygame.KEYDOWN:
            key_down_event = event
            if event.key == pygame.K_r:
                rotate_component_connections(dragged_component, selected_comps_wires, selected_components, selected_wires, zoom_factor, bounding_rectangle, raw_offsets_comp, raw_offsets_line)
            if event.key == pygame.K_DELETE:
                if dragged_component:                   
                    if not adding_component and not copy_dragged_comp:
                        cntrl_z_function(components, connections, timeline, zoom_factor, dragged_component, data_2=None, action_type='removed_component', undo_or_log='log')
                    update_component_name(components, dragged_component, var = False)
                    dragged_component = None  # Remove the dragged component
                    adding_component = False
                    copy_dragged_comp = False
                    start_pos_selecting_rect = None 
                    
                if selected_comps_wires:
                    if not pasted:
                        cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='removed_components_and_connections', undo_or_log='log')
                    update_component_name(components, dragged_component, var = True)
                    selected_components.clear()
                    selected_wires.clear()  
                    pasted = False   
            if event.key == pygame.K_BACKSPACE:
                if dragged_component:
                    if not adding_component and not copy_dragged_comp:
                        cntrl_z_function(components, connections, timeline, zoom_factor, dragged_component, data_2=None, action_type='removed_component', undo_or_log='log')
                    update_component_name(components, dragged_component, var = False)
                    dragged_component = None  # Remove the dragged component
                    adding_component = False 
                    copy_dragged_comp = False
                    start_pos_selecting_rect = None
                if selected_comps_wires:
                    if not pasted:
                        cntrl_z_function(components, connections, timeline, zoom_factor, selected_components, selected_wires, action_type='removed_components_and_connections', undo_or_log='log')
                    update_component_name(components, dragged_component, var = True)
                    selected_components.clear()
                    selected_wires.clear() 
                    pasted = False                              
            if event.key == pygame.K_LALT:
                alt_button = True

            if event.key == pygame.K_ESCAPE:
                drawing_line = False 
                mouse_in_hotzone = False
                current_line = subConnection()  # Reset the line 
                esc_button = True

            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_button = True  

            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_button = True       

            if event.key == pygame.K_z:
                z_button = True

            if event.key == pygame.K_y:   
                y_button = True 

            if event.key == pygame.K_a:   
                a_button = True  

            if event.key == pygame.K_c:   
                c_button = True      

            if event.key == pygame.K_v:   
                v_button = True  

            if event.key == pygame.K_m:   
                m_button = True                  
            
            if not menu_is_open:
                if z_button and ctrl_button and not shift_button:
                    # CTRL + Z
                    if not dragged_component and not selected_comps_wires:
                        cntrl_z_function(components, connections, timeline, zoom_factor, data=None, data_2=None, action_type=None, undo_or_log='undo')
                        update_component_name(components, dragged_component, var = True)
                if z_button and ctrl_button and shift_button:
                    # CTRL + SHIFT + Z
                    if not dragged_component and not selected_comps_wires:
                        cntrl_z_function(components, connections, timeline, zoom_factor, data=None, data_2=None, action_type=None, undo_or_log='undo_undo')
                        update_component_name(components, dragged_component, var = True)
                if y_button and ctrl_button:
                    if not dragged_component and not selected_comps_wires:
                        cntrl_z_function(components, connections, timeline, zoom_factor, data=None, data_2=None, action_type=None, undo_or_log='undo_undo')
                        update_component_name(components, dragged_component, var = True)
                if ctrl_button and c_button:
                    copied_components.clear()
                    copied_wires.clear()
                    copied_component = None
                    if selected_comps_wires:
                        for comp in selected_components:
                            copied_components.append(comp)
                        for conn in selected_wires:
                            copied_wires.append(conn)
                    if dragged_component: 
                        copied_component = dragged_component

                if ctrl_button and v_button and not selected_comps_colliding and not selected_lines_colliding and not comp_is_colliding: 
                    cntrl_v = True
                    copy_dragged_comp, placed_comp, placed_components = placing_component(dragged_component, selected_components, selected_wires, selected_comps_wires, comp_is_colliding, selected_comps_colliding, selected_lines_colliding, adding_component, components, connections, timeline, copy_dragged_comp, zoom_factor, left_mouse_button_place_comp, continious_left_mouse_button, alt_button, left_mouse_button, pasted, esc_button, cntrl_v)  
                    cntrl_v = False 
                    if placed_comp:
                        adding_component = False
                        dragged_component = None
                        left_mouse_button_place_comp = False
                        pasted = False                          
                    if placed_components:
                        bounding_rectangle_meassurements = None
                        bounding_rectangle = None   
                        left_mouse_button_place_comp = False
                        selected_comps_wires = False
                        pasted = False
                    if not selected_comps_wires:    
                        if copied_components or copied_wires:
                            for comp in copied_components:
                                selected_components.append(comp.copy_with_new_id())
                            for conn in copied_wires:
                                selected_wires.append(conn.copy_with_new_id())
                            raw_offsets_comp.clear()
                            raw_offsets_line.clear()
                            bounding_rectangle_meassurements, bounding_rectangle = calculate_bounding_rectangle(selected_components, selected_wires, camera_offset_x, camera_offset_y, zoom_factor) 
                            center_point = bounding_rectangle.center
                            drag_point = snap_to_grid(center_point[0], center_point[1]) 
                            selected_comps_wires =  True
                            for comp in selected_components:
                                offset = drag_point[0] - comp.x, drag_point[1] - comp.y
                                raw_offsets_comp.append(offset)  
                            for wire in selected_wires:
                                start_offset = (drag_point[0] - wire.start_pos[0], drag_point[1] - wire.start_pos[1])
                                end_offset = (drag_point[0] - wire.end_pos[0], drag_point[1] - wire.end_pos[1])
                                raw_offsets_line.append((start_offset, end_offset))     
                            pasted = True
                            
                    if not dragged_component and copied_component and not selected_comps_wires:
                        dragged_component = copied_component.copy_with_new_id() 
                        copy_dragged_comp = True 
                        pasted = True    

        elif event.type == pygame.KEYUP: 
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_button = False

            if event.key == pygame.K_LALT:
                alt_button = False  

            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_button = False

            if event.key == pygame.K_z:
                z_button = False    

            if event.key == pygame.K_y:
                y_button = False 

            if event.key == pygame.K_a:   
                a_button = False  

            if event.key == pygame.K_c:   
                c_button = False

            if event.key == pygame.K_v:   
                v_button = False    

            if event.key == pygame.K_ESCAPE:
                esc_button = False   

            if event.key == pygame.K_m:   
                m_button = False       

    

    if not menu_is_open:    
        selected_connection_color, hand_cursor = select_connection_color(mouse_pos, left_mouse_button, adding_component, hand_cursor)

        hide_menu, hand_cursor = hide_component_menu(mouse_pos, left_mouse_button, hide_menu, hand_cursor)
        
        if dragged_component:  
            drawing_line = False
            mouse_in_hotzone = False  
            current_line = subConnection()  # Reset the line 

        if mouse_in_hotzone and remember_hotzone_pos and not mouse_in_ui and Click_time <= selectingbox_timer and left_mouse_button_up and not dragged_component and not selected_comps_wires and not hovering_over_comp and not hand_cursor and not shift_button:         
            current_line.get_start_pos_connection(remember_hotzone_pos, zoom_factor)
            drawing_line = True
            remember_hotzone_pos = None
            mouse_in_hotzone = False 
        if not mouse_in_hotzone and current_line.end_pos and drawing_line and not line_is_colliding and not adding_component and not mouse_in_ui and not shift_button and left_mouse_button and not dragged_component:                                        
            if current_line.start_pos and current_line.end_pos:
                cntrl_z_function(components, connections, timeline, zoom_factor, current_line, data_2=None, action_type='added_connection', undo_or_log='log')            
                connections.append(current_line) 
                new_line = current_line
                current_line = subConnection()  # Reset the line 
            current_line.get_start_pos_connection(new_line.end_pos, zoom_factor)
            current_line.update_end_pos_connection(virtual_mouse_pos, zoom_factor)  
        
        if not comp_is_colliding and not drawing_line and not mouse_in_ui and not selected_comps_wires and not comp_name and not saved_comp and not shift_button and (left_mouse_button or right_mouse_button):
            # Check if a placed component is clicked
            dragged_component, copy_dragged_comp, adding_component, right_clicked_comp = clicked_on_component(dragged_component, connections, components, virtual_mouse_pos, alt_button, timeline, copy_dragged_comp, zoom_factor, adding_component, right_mouse_button)

        if dragged_component and not adding_component and left_mouse_button:
            raw_offsets_dragged_comp = mouse_pos_dragged_comp[0] - dragged_component.x, mouse_pos_dragged_comp[1] - dragged_component.y  

        if dragged_component and adding_component and copy_dragged_comp and left_mouse_button:
            raw_offsets_dragged_comp = mouse_pos_dragged_comp[0] - dragged_component.x, mouse_pos_dragged_comp[1] - dragged_component.y 

        if dragged_component and adding_component and copy_dragged_comp and not continious_left_mouse_button and comp_is_colliding:
            dragged_component = None
            adding_component = False
            copy_dragged_comp = False     
            comp_is_colliding = False

    draw_virtual_grid(screen, camera_offset_x, camera_offset_y, zoom_factor) 
    
    if not menu_is_open:
        if dragged_component and not selected_comps_wires:
            dragged_component.draw(camera_offset_x, camera_offset_y)
            comp_is_colliding = check_component_collision(dragged_component, components, connections)
            if comp_is_colliding:
                dragged_component.color = RED
            else:
            # Reset to the original image
                dragged_component.color = SELECTEDCOMP     

        if (selected_comps_wires or dragged_component) and not shift_button:
            replace_selected_components_and_connections(adding_component, dragged_component, raw_offsets_dragged_comp[0], raw_offsets_dragged_comp[1], camera_offset_x, camera_offset_y, selected_components, selected_wires, selected_comps_wires, raw_offsets_comp, raw_offsets_line, mouse_pos, zoom_factor, continious_left_mouse_button, copy_dragged_comp, virtual_selecting_box, pasted) 
            if selected_comps_wires and not virtual_selecting_box:
                bounding_rectangle_meassurements, bounding_rectangle = calculate_bounding_rectangle(selected_components, selected_wires, camera_offset_x, camera_offset_y, zoom_factor) 

        if not shift_button and not mouse_in_ui and (selected_comps_wires or dragged_component):
            copy_dragged_comp, placed_comp, placed_components = placing_component(dragged_component, selected_components, selected_wires, selected_comps_wires, comp_is_colliding, selected_comps_colliding, selected_lines_colliding, adding_component, components, connections, timeline, copy_dragged_comp, zoom_factor, left_mouse_button_place_comp, continious_left_mouse_button, alt_button, left_mouse_button, pasted, esc_button, cntrl_v)  
            if placed_comp:
                adding_component = False
                edit_component_props = dragged_component
                dragged_component = None
                left_mouse_button_place_comp = False
                pasted = False
                placed_comp_is_saved_comp = False
            elif placed_components:
                bounding_rectangle_meassurements = None
                bounding_rectangle = None   
                left_mouse_button_place_comp = False
                pasted = False         

    
    
    hovering_over_comp = draw_existing_components(components, selected_components, virtual_mouse_pos, dragged_component, selected_comps_wires, drawing_line, camera_offset_x, camera_offset_y, continious_left_mouse_button, zoom_factor)
    draw_existing_connections(connections, selected_wires, camera_offset_x, camera_offset_y, continious_left_mouse_button, virtual_mouse_pos)
    if not menu_is_open:
        if not dragged_component and not selected_comps_wires and not mouse_in_ui and not menu_is_open and not drawing_line and not left_mouse_button and not hovering_over_comp and not continious_left_mouse_button and not hand_cursor:
            remember_hotzone_pos, mouse_in_hotzone = get_and_draw_hotzone_pos_at_mouse_pos(virtual_mouse_pos, camera_offset_x, camera_offset_y, zoom_factor)
        if current_line.start_pos and drawing_line:
            current_line.update_end_pos_connection(virtual_mouse_pos, zoom_factor)
            current_line.color = selected_connection_color
            line_is_colliding = current_line.draw_current_line(camera_offset_x, camera_offset_y, components, connections, selected_connection_color, zoom_factor)    
        elif not drawing_line:
            line_is_colliding = False
        if start_pos_selecting_rect and continious_left_mouse_button and (pygame.time.get_ticks() - Click_time) > selectingbox_timer and not dragged_component and not shift_button and not drawing_line and not alt_button:
            virtual_selecting_box = create_and_draw_selecting_box(start_pos_selecting_rect, virtual_mouse_pos, camera_offset_x, camera_offset_y, zoom_factor)
            remember_hotzone_pos = None
            mouse_in_hotzone = False
        if (continious_left_mouse_button and not shift_button and not alt_button and not left_mouse_button_place_comp and start_pos_selecting_rect and virtual_selecting_box) or (ctrl_button and a_button):
            selecting_components_and_lines(virtual_selecting_box, selected_components, selected_wires, components, connections, ctrl_button, a_button, timeline, zoom_factor)
        if selected_comps_wires: 
            selected_comps_colliding, selected_lines_colliding = draw_selected_components_and_connections(components, connections, selected_components, selected_wires, camera_offset_x, camera_offset_y, start_pos_selecting_rect)
        if selected_comps_wires and bounding_rectangle_meassurements:
            draw_bounding_rectangle(bounding_rectangle_meassurements)
 
    draw_collision_circles(components, connections, camera_offset_x, camera_offset_y, zoom_factor)
    draw_Ui(hide_menu, is_teacher)
    loaded_components, loaded_connections, hand_cursor = newFile(mouse_pos, left_mouse_button, components, connections, hand_cursor)
    show_project_name()

   
    

    hand_cursor = save_button(components, connections, mouse_pos, left_mouse_button, menu_is_open, key_down_event, hand_cursor)
    hand_cursor = save_as_button(mouse_pos, left_mouse_button, components, connections, menu_is_open, hand_cursor)
    hand_cursor = new_file_button(mouse_pos, left_mouse_button, components, connections, menu_is_open, hand_cursor)
   
    imported_components, imported_connections, hand_cursor = import_project(mouse_pos, left_mouse_button, menu_is_open, hand_cursor)

    if imported_components or imported_connections:
        selected_components, selected_comps_wires = imported_components, imported_connections
        selected_wires = imported_connections

        raw_offsets_comp.clear()
        raw_offsets_line.clear()
        bounding_rectangle_meassurements, bounding_rectangle = calculate_bounding_rectangle(selected_components, selected_wires, camera_offset_x, camera_offset_y, zoom_factor) 
        center_point = bounding_rectangle.center
        end_pos_selecting_rect = snap_to_grid(center_point[0], center_point[1]) 
        for comp in selected_components:
            offset = end_pos_selecting_rect[0] - comp.x, end_pos_selecting_rect[1] - comp.y
            raw_offsets_comp.append(offset)  
        for wire in selected_wires:
            start_offset = (end_pos_selecting_rect[0] - wire.start_pos[0], end_pos_selecting_rect[1] - wire.start_pos[1])
            end_offset = (end_pos_selecting_rect[0] - wire.end_pos[0], end_pos_selecting_rect[1] - wire.end_pos[1])
            raw_offsets_line.append((start_offset, end_offset))
        pasted = True
        imported_components = None
        imported_connections = None
                 
    if not loaded_components and not loaded_connections:
        
        loaded_components, loaded_connections, hand_cursor = load_project(mouse_pos, left_mouse_button, components, connections, menu_is_open, hand_cursor)

    if loaded_components or loaded_connections:
        components = loaded_components
        connections = loaded_connections
        loaded_components = None
        loaded_connections = None
        timeline_cntrl_shift_z = []
        timeline = [] 



    if not hide_menu:    
        comp_name, saved_comp, hand_cursor = componentMenus(event ,mouse_pos, screen, new_height, adding_component, selected_comps_wires, dragged_component, virtual_selecting_box, menu_is_open, hand_cursor) 

    if (placed_comp and hasattr(edit_component_props, "properties") and not edit_component_props.edited and not placed_comp_is_saved_comp) or (right_clicked_comp and hasattr(right_clicked_comp, "properties")):
            
            if right_clicked_comp:
                edit_component_props = right_clicked_comp
            saved_component, hand_cursor = properties_menu(edit_component_props, left_mouse_button, mouse_pos, key_down_event, hand_cursor)

   
    if saved_component:
        edit_component_props = None
        right_clicked_comp = None
        if saved_component is not 1:
            save_component(saved_component)
        saved_component = None
    

    

    if comp_name and left_mouse_button or wasFeedbackBlock:
        dragged_component = globals()[comp_name]() 
        scale_newly_added_component(dragged_component, zoom_factor)       
        drag_offset_x = dragged_component.scale_x // 2
        drag_offset_y = dragged_component.scale_y // 2
        drag_offset_x, drag_offset_y = snap_to_virtual_grid(drag_offset_x, drag_offset_y, zoom_factor)
        raw_offsets_dragged_comp = (drag_offset_x / (SPACING + zoom_factor)) * SPACING, (drag_offset_y / (SPACING + zoom_factor)) * SPACING
        adding_component = True
        wasFeedbackBlock = None
    elif saved_comp and left_mouse_button:
        dragged_component = saved_comp.copy_with_new_id()
        scale_newly_added_component(dragged_component, zoom_factor)   
        drag_offset_x = dragged_component.scale_x // 2
        drag_offset_y = dragged_component.scale_y // 2
        drag_offset_x, drag_offset_y = snap_to_virtual_grid(drag_offset_x, drag_offset_y, zoom_factor)
        raw_offsets_dragged_comp = (drag_offset_x / (SPACING + zoom_factor)) * SPACING, (drag_offset_y / (SPACING + zoom_factor)) * SPACING
        adding_component = True
        placed_comp_is_saved_comp = True
    
    if hand_cursor or hovering_over_comp:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 
        
    open_manual(key_down_event)
    shortcuts(mouse_pos)

    if not start_menu_is_open and not logged_user:
        remember_hotzone_pos = None
        mouse_in_hotzone = False                                                                                                       
        userdetails = draw_login_register_menu(key_down_event, mouse_pos, left_mouse_button)
        if userdetails and len(userdetails) == 3:
            logged_user, user_id, is_teacher = userdetails
    loggedout = logout(mouse_pos, left_mouse_button)
    show_user(logged_user, is_teacher)

    if loggedout:
        logged_user = None
        loggedout = False
        user_id = None
        is_teacher = None
    class_menu_open, loaded_components, loaded_connections = manage_classes_button(mouse_pos, left_mouse_button, user_id, key_down_event, logged_user, is_teacher)

    get_feedback(components, virtual_mouse_pos, dragged_component, selected_comps_wires, drawing_line, left_mouse_button, key_down_event)

    upload_feedback(mouse_pos, left_mouse_button, components, connections)
    logo()
    hand_cursor = False     

    left_mouse_button = False 
    left_mouse_button_up = False
    right_mouse_button = False
    key_down_event = None

    if class_menu_open:
        remember_hotzone_pos = None
        mouse_in_hotzone = False  
        
    if loaded_components or loaded_connections:
        components = loaded_components
        connections = loaded_connections
        loaded_components = None
        loaded_connections = None
        timeline_cntrl_shift_z = []
        timeline = [] 
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

