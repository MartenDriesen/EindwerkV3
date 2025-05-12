import pygame
import json
import os
from uuid import UUID
from tkinter import Tk, filedialog
import time

from main.global_constants import screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, LIGHT_BLUE
from component_classes.subConnection import subConnection
from functions.save_to_mongodb import save_project_to_mongodb

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

from main.global_constants import font2
# Initialize Pygame
pygame.init()

# Initialize variables
input_active = False
input_rename_active = False
rename_menu_visible = False
new_file_menu_visible = False
name_new_file_menu_visible = False
saving_notification = False
new_project_name = ""
start_menu_visible = True
inputred = False
menu_is_open = False

filename = None
is_saved = None
is_not_saved = None
is_saved_before_new_file = None
is_not_saved_before_new_file = None
projectname_is_reset = False
old_components = []
old_connections = []

projectname = ""
file_path = ""
projectname_bool = ""

def newFile(mouse_pos, left_mouse_button, current_components, current_connections, hand_cursor):
    global projectname, start_menu_visible, new_file_menu_visible, menu_is_open

    loaded_components, loaded_connections = None, None

    # Load and scale menu image
    start_file_menu = pygame.image.load("./images/menus/start.png")
    start_file_menu = pygame.transform.smoothscale(start_file_menu, (480, 100))

    # Text strings
    new_project = "New file"
    load_project = "Load file"
    powerlink = "Powerlink"

    # Render text
    new_project_text = font2.render(new_project, True, WHITE)
    load_project_text = font2.render(load_project, True, WHITE)
    powerlink_text = font2.render(powerlink, True, WHITE)

    # Positioning text
    
    powerlink_text_rect = powerlink_text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 20))

    # Define button rectangles with padding
    

    # Define menu rectangle
    start_file_menu_rect = pygame.Rect(
        (SCREEN_WIDTH / 2) - 240,
        (SCREEN_HEIGHT / 2) - 50,
        start_file_menu.get_width(),
        start_file_menu.get_height()
    )

    # Persistent red background state
    if "background_draw_time" not in globals():
        global background_draw_time
        background_draw_time = 0

    # Handle mouse interactions
    

    # Draw menu if visible
    if start_menu_visible:

       
        new_project_text_rect = new_project_text.get_rect(center=((SCREEN_WIDTH / 2) + 125, (SCREEN_HEIGHT / 2) + 20))
        load_project_text_rect = load_project_text.get_rect(center=((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) + 20))
        new_project_button_rect = new_project_text_rect.inflate(10, 10)  # Add 10px padding to width and height
        load_project_button_rect = load_project_text_rect.inflate(10, 10)  # Add 10px padding to width and height
        menu_is_open = True
        
        # Check if the red background should be drawn
        current_time = time.time()
        if current_time - background_draw_time <= 1:  # Keep red background for 1 second
            pygame.draw.rect(screen, RED, start_file_menu_rect)  # Red rectangle behind the menu

        # Draw the menu on top of the red background
        screen.blit(start_file_menu, start_file_menu_rect)

        # Draw light blue buttons
        pygame.draw.rect(screen, LIGHT_BLUE, new_project_button_rect, border_radius=5)  # Light blue color
        pygame.draw.rect(screen, LIGHT_BLUE, load_project_button_rect, border_radius=5)  # Light blue color

        # Draw text on top of buttons
        screen.blit(new_project_text, new_project_text_rect)
        screen.blit(load_project_text, load_project_text_rect)
        screen.blit(powerlink_text, powerlink_text_rect)

        if load_project_button_rect.collidepoint(mouse_pos) or new_project_button_rect.collidepoint(mouse_pos):
            hand_cursor = True

        if left_mouse_button:
            if start_file_menu_rect.collidepoint(mouse_pos):  # Ensure clicks are inside the menu area
                if new_project_button_rect.collidepoint(mouse_pos):
                    start_menu_visible = False
                    projectname = "new document"
                    show_project_name()
                elif load_project_button_rect.collidepoint(mouse_pos): 
                    # Call load_file_explorer only once and update state
                    loaded_components, loaded_connections = load_file_explorer(current_components, current_connections)
                    if loaded_components or loaded_connections:
                        start_menu_visible = False  # Close the start menu after successful loading
                        print("Project loaded successfully.")
            else:
                # Flag to draw a red rectangle behind the menu
                background_draw_time = time.time()  # Update background draw time
    else:
        menu_is_open = False
    
        
    return loaded_components, loaded_connections, hand_cursor

def show_project_name():
    global projectname  # Ensure projectname is accessed globally

    project = f"Project: {projectname}"  # Format string to show project name

    project_text = font2.render(project, True, WHITE)  # Render with highlight color
    project_rect = pygame.Rect((SCREEN_WIDTH / 2) - 100, 12, 200, 30)  # Position the project name text

    # Render the project name text on the screen
    screen.blit(project_text, project_rect)




def save_button(data_comps, data_lines, mouse_pos, left_mouse_button, menu_is_open_passed, event, hand_cursor, feedback):
    global saving_notification

    mouse_x, mouse_y = mouse_pos

    # Render save button
    save = "save local"
    save_text = font2.render(save, True, WHITE)
    save_rect = pygame.Rect(170, 12, 40, 30)
    screen.blit(save_text, save_rect)
    
    if event:
        if event.key == pygame.K_s and pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
            saving_file(data_comps, data_lines)
    # Check for mouse click on save button
    if save_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button and not menu_is_open_passed:
        saving_file(data_comps, data_lines)
       
    if saving_notification:
        saving_file_notification()
    if save_rect.collidepoint(mouse_x, mouse_y):
        hand_cursor = True

    return hand_cursor     

def new_file_button(mouse_pos, left_mouse_button, current_components, current_connections, menu_is_open_passed, hand_cursor):
    global is_saved_before_new_file, is_not_saved_before_new_file, name_new_file_menu_visible, projectname

    mouse_x, mouse_y = mouse_pos

    new_file = "new file"
    new_file_text = font2.render(new_file, True, WHITE)
    new_file_rect = pygame.Rect(80, 12, 40, 30)
    screen.blit(new_file_text, new_file_rect)

    if new_file_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button and not menu_is_open_passed:
        check_if_saved_for_new_file(current_components, current_connections)

    if is_not_saved_before_new_file:
        # User has unsaved changes, ask whether to save
        user_decision, hand_cursor = unsaved_changes_menu(mouse_pos, current_components, current_connections, left_mouse_button, hand_cursor)

        if user_decision == "no":
            # If user chooses "No", proceed to open the "new file" menu
            projectname = "new document"
            show_project_name()
            current_components.clear()
            current_connections.clear()
            is_not_saved_before_new_file = None
        elif user_decision == "yes":
            # If user chooses "Yes", save the file first, then proceed to open the "new file" menu
            saving_file(current_components, current_connections)
            projectname = "new document"
            current_components.clear()
            current_connections.clear()
            show_project_name()
            is_not_saved_before_new_file = None
        elif user_decision == "cross":
            is_not_saved_before_new_file = None

    if is_saved_before_new_file:
        # No unsaved changes, directly open the "new file" menu
        projectname = "new document"
        show_project_name()
        current_components.clear()
        current_connections.clear()
        is_saved_before_new_file = None  

    if new_file_rect.collidepoint(mouse_x, mouse_y):
        hand_cursor = True

    return hand_cursor

 
    
def check_if_saved_for_new_file(current_components, current_connections):
    global  is_saved_before_new_file, is_not_saved_before_new_file, old_connections, old_components

    # Check if there are unsaved changes
    if (current_components != old_components) or \
        (current_connections != old_connections):
        is_not_saved_before_new_file = True
    else:
        is_saved_before_new_file = True


def saving_file(data_comps, data_lines):

    global projectname, file_path, saving_notification


    print(file_path, "exists")

    # Check if file exists in the current directory
    if os.path.exists(file_path):
        # If file exists, save it directly
        save_project_data(file_path, data_comps, data_lines)
        print(f"File already exists, saved directly to {projectname}")
        saving_notification = True
    else:
        # If file does not exist, show file explorer to let user choose location
        save_file_explorer(data_comps, data_lines)

def save_file_explorer(data_comps, data_lines):
    global projectname, file_path, saving_notification
    print(data_comps)
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window

    sanitized_name = projectname.strip() if projectname.strip() else "untitled_project"
    file_path = filedialog.asksaveasfilename(
        initialfile=sanitized_name,  # Use sanitized project name as the default file name
        defaultextension=".pl",
        filetypes=[("Project files", "*.pl"), ("All files", "*.*")]
    )
    print(file_path, "given")

    if file_path:  # Check if a file path was selected
        # Save data after user selects a location
        save_project_data(file_path, data_comps, data_lines)
        print(f"File saved successfully at {file_path}")
        
        # Extract the project name from the file path (remove directory and extension)
        projectname = file_path.split("/")[-1].split(".")[0]
        
        # Call show_project_name to display the updated project name
        show_project_name()

        # Trigger saving notification
        saving_notification = True
        
    # Make sure to quit and destroy the Tkinter root window to regain control of the application
    root.quit()
    root.destroy()

# Function to handle saving project data

def save_project_data(projectpath, data_comps, data_lines):
    # Serialize each component with its class name
    global old_components, old_connections
    serialized_comps = []

    for comp in data_comps:
        comp_data = comp.__dict__.copy()
        # Convert UUID to string, if present
        if isinstance(comp_data.get('id'), UUID):
            comp_data['id'] = str(comp_data['id'])
        comp_data['class_name'] = comp.__class__.__name__  # Store the class name
        serialized_comps.append(comp_data)

    print(serialized_comps)  # Debug print serialized components

    # Serialize each connection with its class name
    serialized_connections = []

    for conn in data_lines:
        conn_data = conn.__dict__.copy()
        # Convert UUID to string, if present
        if isinstance(conn_data.get('id'), UUID):
            conn_data['id'] = str(conn_data['id'])
        conn_data['class_name'] = conn.__class__.__name__  # Store the class name
        serialized_connections.append(conn_data)

    # Save data as a list of lists
    project_data = [serialized_comps, serialized_connections]

    # Debug print the full project data being saved
    try:
        with open(projectpath, 'w') as file:
            json.dump(project_data, file, indent=4)
            old_components = data_comps.copy()
            old_connections = data_lines.copy()
    except Exception as e:
        print(f"Failed to save file: {e}")
    
    projectname = projectpath.split("/")[-1].split(".")[0]
    save_project_to_mongodb(projectname, data_comps, data_lines)

def load_project(mouse_pos, left_mouse_button, current_components, current_connections, menu_is_open_passed, hand_cursor):
    global is_saved, is_not_saved, old_components # Declare as global here

    loaded_components, loaded_connections = None, None
    mouse_x, mouse_y = mouse_pos
    # Render load button
    load = "load file"
    load_text = font2.render(load, True, WHITE)
    load_text_rect = pygame.Rect(350, 12, 80, 30)  # Adjusted rect size to fit "load file"
    screen.blit(load_text, load_text_rect)

    # Check for mouse click on load button
    if load_text_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button and not menu_is_open_passed:
         check_if_saved(current_components, current_connections)

    if  is_not_saved:
        # User has unsaved changes, ask whether to save
        user_decision, hand_cursor = unsaved_changes_menu(mouse_pos, current_components, current_connections, left_mouse_button, hand_cursor)

        if user_decision == "no":
            # If user chooses "No", proceed to load a file
              # Mark as file loaded
            loaded_components, loaded_connections = load_file_explorer(current_components, current_connections)
            is_not_saved = None
        elif user_decision == "yes":
            # If user chooses "Yes", save the file first, then proceed to load a file
              # Mark as file loaded
            loaded_components, loaded_connections = load_file_explorer(current_components, current_connections)
            is_not_saved = None
    if is_saved:  # Ensure this only triggers if file is not loaded
        # No unsaved changes, directly load a file
          # Mark as file loaded
        loaded_components, loaded_connections = load_file_explorer(current_components, current_connections)
        is_saved = None
    
    if load_text_rect.collidepoint(mouse_x, mouse_y):
        hand_cursor = True

    return loaded_components, loaded_connections, hand_cursor


def unsaved_changes_menu(mouse_pos, current_components, current_connections, left_mouse_button, hand_cursor):
    global is_saved, menu_is_open

    mouse_x, mouse_y = mouse_pos
    menu_is_open = True

    # Load and scale menu background image
    save_file_menu = pygame.image.load("./images/menus/start.png")
    save_file_menu = pygame.transform.smoothscale(save_file_menu, (480, 100))

    cross = pygame.image.load("./images/icons/cross.png")
    cross = pygame.transform.smoothscale(cross, (10, 10))

    cross_rect = cross.get_rect(center=((SCREEN_WIDTH / 2) + 205, (SCREEN_HEIGHT / 2) - 22))
    # Text strings
    yes = "Yes"
    no = "No"
    changes = "You have unsaved changes, Do you want to save file?"

    # Render text
    yes_text = font2.render(yes, True, WHITE)
    no_text = font2.render(no, True, WHITE)
    changes_text = font2.render(changes, True, WHITE)

    # Positioning text
    yes_text_rect = yes_text.get_rect(center=((SCREEN_WIDTH / 2) + 125, (SCREEN_HEIGHT / 2) + 20))
    no_text_rect = no_text.get_rect(center=((SCREEN_WIDTH / 2) - 150, (SCREEN_HEIGHT / 2) + 20))
    changes_text_rect = changes_text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 20))

    # Define button rectangles with padding
    yes_button_rect = yes_text_rect.inflate(10, 10)  # Add 10px padding to width and height
    no_button_rect = no_text_rect.inflate(10, 10)    # Add 10px padding to width and height

    # Define menu rectangle
    save_file_menu_rect = pygame.Rect(
        (SCREEN_WIDTH / 2) - 240,
        (SCREEN_HEIGHT / 2) - 50,
        save_file_menu.get_width(),
        save_file_menu.get_height()
    )

    # Persistent red background state
    if "background_draw_time" not in globals():
        global background_draw_time
        background_draw_time = 0

    # Check for user interaction
    if left_mouse_button:
        if yes_button_rect.collidepoint(mouse_x, mouse_y):
            # User clicked "Yes", save the file first
            saving_file(current_components, current_connections)
            menu_is_open = False
            return "yes", hand_cursor  # Return decision after saving, proceed to load file
        elif no_button_rect.collidepoint(mouse_x, mouse_y): 
            # User clicked "No", proceed to load the file
            menu_is_open = False
            return "no", hand_cursor  # Return decision
        elif cross_rect.collidepoint(mouse_pos): 
            menu_is_open = False
            return "cross", hand_cursor
        elif not save_file_menu_rect.collidepoint(mouse_x, mouse_y):
            # User clicked outside the menu
            background_draw_time = time.time()

    # Render red rectangle behind the menu if flagged
    current_time = time.time()
    if current_time - background_draw_time <= 1:  # Keep red background for 1 second
        pygame.draw.rect(screen, RED, save_file_menu_rect)  # Draw red rectangle

    # Render menu background
    screen.blit(save_file_menu, save_file_menu_rect)

    # Draw light blue buttons behind text
    pygame.draw.rect(screen, LIGHT_BLUE, yes_button_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_BLUE, no_button_rect, border_radius=5)

    # Render text on top of buttons
    screen.blit(cross, cross_rect)
    screen.blit(yes_text, yes_text_rect)
    screen.blit(no_text, no_text_rect)
    screen.blit(changes_text, changes_text_rect)
    
    if cross_rect.collidepoint(mouse_pos) or no_button_rect.collidepoint(mouse_x, mouse_y) or yes_button_rect.collidepoint(mouse_x, mouse_y):
        hand_cursor = True
    return None, hand_cursor

def check_if_saved(current_components, current_connections):
    global  is_saved, is_not_saved, old_connections, old_components

    # Check if there are unsaved changes
    if (current_components != old_components) or \
        (current_connections != old_connections):
        is_not_saved = True
        print("is_not_saved",is_not_saved)
    else:
        is_saved = True
        print("is_saved",is_saved)
       

def load_file_explorer(current_components, current_connections):
    global old_components, old_connections, start_menu_visible, projectname, file_path

    # Define the registry of component classes
    component_classes = {
        "AC_Motor": AC_Motor,
        "DC_Motor": DC_Motor,
        "Capacitor": Capacitor,
        "Current_Meter": Current_Meter,
        "AC_Voltage_Src": AC_Voltage_Src,
        "DC_Voltage_Src": DC_Voltage_Src,
        "Diode": Diode,
        "Fuse": Fuse,
        "IGBT_N_Channel": IGBT_N_Channel,
        "IGBT_P_Channel": IGBT_P_Channel,
        "Inductor": Inductor,
        "JFET_N_Channel": JFET_N_Channel,
        "JFET_P_Channel": JFET_P_Channel,
        "LDR": LDR,
        "LED": LED,
        "MOSFET_N_Depl": MOSFET_N_Depl,
        "MOSFET_N_Enhance": MOSFET_N_Enhance,
        "MOSFET_P_Depl": MOSFET_P_Depl,
        "MOSFET_P_Enhance": MOSFET_P_Enhance,
        "Normally_Open_Switch": Normally_Open_Switch,
        "Normally_Closed_Switch": Normally_Closed_Switch,
        "NPN_Transistor": NPN_Transistor,
        "PNP_Transistor": PNP_Transistor,
        "Polar_Capacitor": Polar_Capacitor,
        "Potentiometer": Potentiometer,
        "Battery": Battery,
        "Normally_Open_Relay": Normally_Open_Relay,
        "Normally_Closed_Relay": Normally_Closed_Relay,
        "Resistor": Resistor,
        "Schottky_Diode": Schottky_Diode,
        "SCR": SCR,
        "Thermistor": Thermistor,
        "Transformer": Transformer,
        "Triac": Triac,
        "Var_Capacitor": Var_Capacitor,
        "Var_Inductor": Var_Inductor,
        "Var_Polar_Capacitor": Var_Polar_Capacitor,
        "Varistor": Varistor,
        "Volt_Meter": Volt_Meter,
        "Power_Meter": Power_Meter,
        "Zener_Diode": Zener_Diode,
        "Three_Phase_Motor_Delta": Three_Phase_Motor_Delta,
        "Three_Phase_Motor_Star": Three_Phase_Motor_Star,
        "Three_Phase_Power_Src": Three_Phase_Power_Src,
        "Ground": Ground,
        "Photo_Diode": Photo_Diode,
        "Teleruptor": Teleruptor,
        "Three_Way_Switch": Three_Way_Switch,
        "Four_Way_Switch": Four_Way_Switch,
        "SPS_Open": SPS_Open,
        "DPST": DPST,
        "DPST_Open": DPST_Open,
        "SPST": SPST,
        "TPST_Open": TPST_Open,
        "Staircase_Timer_Auto": Staircase_Timer_Auto,
        "Circuit_Breaker": Circuit_Breaker,
        "Connection": Connection
    }

    try:
        print("Opening file dialog...")
        root = Tk()
        root.withdraw()  # Hide the Tkinter root window

        file_path = filedialog.askopenfilename(
            title="Load Project File",
            filetypes=[("Project files", "*.pl"), ("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            print("File dialog was canceled, using current components and connections.")
            return current_components, current_connections

        if file_path:
            print(f"File selected: {file_path}")

            with open(file_path, 'r') as file:
                project_data = json.load(file)

            # Load the components and connections
            loaded_components_data = project_data[0]
            loaded_connections_data = project_data[1]  # Assuming connections are at index 1

            # Rebuild the component objects from the loaded data
            loaded_components = []
            for comp_data in loaded_components_data:
                # Get the class based on the saved 'class_name' attribute
                class_name = comp_data.get('class_name')
                component_class = component_classes.get(class_name)  # Match by class name

                if component_class is None:
                    print(f"Unknown component class: {class_name}")
                    continue

                # Instantiate the component and set its attributes
                component = component_class()  # Instantiate the identified class
                for key, value in comp_data.items():
                    if key == 'id':
                        # Convert id back to UUID
                        value = UUID(value)
                    if key != 'class_name':  # Skip the 'class_name' field during deserialization
                        setattr(component, key, value)

                loaded_components.append(component)

            # Rebuild the connection objects from the loaded data
            loaded_connections = []
            for conn_data in loaded_connections_data:
                connection = subConnection()  # Instantiate the Connection class
                for key, value in conn_data.items():
                    if key == 'id':
                        # Convert id back to UUID
                        value = UUID(value)
                    setattr(connection, key, value)  # Set each attribute for the connection
                loaded_connections.append(connection)

            projectname = file_path.split("/")[-1].split(".")[0]  # Extract filename without extension
            print(f"Project name: {projectname}")

            print("updated")
            # Call show_project_name() to display the updated project name
            show_project_name()
            start_menu_visible = False

            if loaded_components or loaded_connections:
                print("components_loaded")
                start_menu_visible = False
                old_components = loaded_components.copy()
                old_connections = loaded_connections.copy()
        # Ensure Tkinter cleanup
        root.quit()
        root.destroy()

    except Exception as e:
        print(f"Failed to load project: {e}")
    # Return the loaded data, whether successful or not
    return loaded_components, loaded_connections

start_timer = None

def saving_file_notification():
    global start_timer, saving_notification
    # Load the save file menu image and scale it
    save_file_menu = pygame.image.load("./images/menus/start.png")
    save_file_menu = pygame.transform.smoothscale(save_file_menu, (480, 100))

    # Text to display
    saving = f"Saving {projectname}"
    saving_text = font2.render(saving, True, WHITE)

    # Get the text rectangle
    saving_text_rect = saving_text.get_rect(center=((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) - 20))

    # Define the notification menu rect
    save_notification_menu_rect = pygame.Rect((SCREEN_WIDTH / 2) - 240, (SCREEN_HEIGHT / 2) - 50, save_file_menu.get_width(), save_file_menu.get_height())

    # Get the current time when the notification is triggered
    if start_timer is None: 
        start_timer = pygame.time.get_ticks() 

    if pygame.time.get_ticks() - start_timer < 1000:  # 1000 milliseconds = 1 second
        # Draw the notification menu
        screen.blit(save_file_menu, save_notification_menu_rect)
        screen.blit(saving_text, saving_text_rect)
    else:
        saving_notification = False
        start_timer = None  

def is_menu_open():
    return menu_is_open


