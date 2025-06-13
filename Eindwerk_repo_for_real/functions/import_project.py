from main.global_constants import font2, WHITE, SCREEN_HEIGHT, screen, SCREEN_WIDTH
import pygame
from component_classes.subConnection import subConnection

from component_classes.Socket import Socket
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
from component_classes.Lamp import Lamp

import json
from uuid import UUID
from tkinter import Tk, filedialog
from uuid import UUID, uuid4

def import_project(mouse_pos, left_mouse_button, menu_is_open, hand_cursor):

    imported_comps, imported_connections = None, None
    
    import_text = font2.render("import", True, WHITE)
    import_text_rect = pygame.Rect(420, 12, 50, 30)

    screen.blit(import_text, import_text_rect)

    if import_text_rect.collidepoint(mouse_pos) and left_mouse_button and not menu_is_open:
       imported_comps, imported_connections = load_file()
    
    if import_text_rect.collidepoint(mouse_pos):
        hand_cursor = True
    return imported_comps, imported_connections, hand_cursor

def load_file():

    loaded_components, loaded_connections = None, None

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
        "Connection": Connection,
        "Socket": Socket,
        "Lamp": Lamp
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
            return None, None

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
                        value = uuid4()
                    setattr(component, key, value)

                loaded_components.append(component)

            # Rebuild the connection objects from the loaded data
                loaded_connections = []
            for conn_data in loaded_connections_data:
                connection = subConnection()  # Instantiate the Connection class
                for key, value in conn_data.items():
                    if key == 'id':
                        # Assign a new unique ID to the connection
                        value = uuid4()
                    setattr(connection, key, value)  # Set each attribute for the connection
                loaded_connections.append(connection)

            print("updated")
            # Call show_project_name() to display the updated project name
        print(loaded_connections)
        # Ensure Tkinter cleanup
        root.quit()
        root.destroy()

    except Exception as e:
        print(f"Failed to load project: {e}")
    # Return the loaded data, whether successful or not
    return loaded_components, loaded_connections