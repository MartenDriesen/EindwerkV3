import pygame
from main.global_constants import DARKBLUE, WHITE, HIGHLIGHT_TEXT_COLOR, BLUETEXT, DROPDOWN_DELAY, font, font2, font3, font4, SCREEN_HEIGHT, SCREEN_WIDTH, screen
# Initialize Pygame
pygame.init()

def load_and_scale_image(image_path, max_width, max_height):
    """
    Load an image and scale it proportionally within the specified max dimensions.
    """
    image = pygame.image.load(image_path)
    original_width, original_height = image.get_size()
    
    # Calculate the scaling factor to keep the aspect ratio
    scale_factor = min(max_width / original_width, max_height / original_height)
    
    # If the image is already smaller than the max dimensions, don't scale up
    if scale_factor < 1:
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        image = pygame.transform.smoothscale(image, (new_width, new_height))
    
    return image

saved_components = []

component_explanations = {
     "Resistor": [
        "Resists current flow.",
        "Used in voltage division.",
        "Basic passive component."
    ],
    "Varistor": [
        "Voltage-dependent resistor.",
        "Protects from surges.",
        "Non-linear resistance."
    ],
    "Thermistor": [
        "Temperature-sensitive resistor.",
        "NTC or PTC types.",
        "Used in sensors."
    ],
    "Capacitor": [
        "Stores electric charge.",
        "Used for filtering.",
        "Two conductive plates."
    ],
    "Variable_Capacitor": [
        "Adjustable capacitance.",
        "Used in tuning circuits.",
        "Rotating plates."
    ],
    "Polarized_Capacitor": [
        "Has polarity (e.g., electrolytic).",
        "Higher capacitance values.",
        "Used in DC circuits."
    ],
    "Variable_Polarized_Capacitor": [
        "Polarized with adjustable value.",
        "Rare component type.",
        "Specialized tuning uses."
    ],
    "Diode": [
        "Allows current in one direction.",
        "Used in rectifiers.",
        "Has a forward voltage."
    ],
    "Schottky_Diode": [
        "Low forward voltage drop.",
        "Fast switching.",
        "Used in power circuits."
    ],
    "Zener_Diode": [
        "Allows reverse current at breakdown.",
        "Used for voltage regulation.",
        "Sharp breakdown voltage."
    ],
    "LED": [
        "Light Emitting Diode.",
        "Needs current limiting.",
        "Used in displays."
    ],
    "Photo_Diode": [
        "Light-sensitive diode.",
        "Generates current with light.",
        "Used in sensors."
    ],
    "Inductor": [
        "Stores energy in magnetic field.",
        "Opposes change in current.",
        "Coil of wire."
    ],
    "Variable_Inductor": [
        "Adjustable inductance.",
        "Used in RF circuits.",
        "Ferrite or air core."
    ],
    "Battery": [
        "DC power source.",
        "Stores chemical energy.",
        "Used in portable devices."
    ],
    "DC_Voltage_Source": [
        "Constant voltage supply.",
        "Polarity sensitive.",
        "Used in electronics."
    ],
    "AC_Voltage_Source": [
        "Alternating current supply.",
        "Polarity alternates.",
        "Used in power systems."
    ],
    "Three_Phase_Power_Source": [
        "Three AC waveforms.",
        "Used in industrial power.",
        "Balanced load supply."
    ],
    "NPN_Transistor": [
        "Current amplifier.",
        "Controlled by base current.",
        "Common in switching."
    ],
    "PNP_Transistor": [
        "Like NPN but reversed.",
        "Base current flows out.",
        "Less common in logic."
    ],
    "MOSFET_N_Channel_Depletion_type": [
        "Normally on device.",
        "Needs negative gate voltage to turn off.",
        "Fast switching."
    ],
    "MOSFET_N_Channel_Enhancement_type": [
        "Normally off device.",
        "Needs positive gate voltage to turn on.",
        "Used in logic circuits."
    ],
    "MOSFET_P_Channel_Depletion_type": [
        "Normally on device.",
        "Gate voltage turns it off.",
        "Rarely used."
    ],
    "MOSFET_P_Channel_Enhancement_type": [
        "Normally off device.",
        "Gate voltage turns it on.",
        "Used with N-channel pairs."
    ],
    "JFET_N_Channel": [
        "Voltage-controlled resistor.",
        "Used in amplifiers.",
        "High input impedance."
    ],
    "JFET_P_Channel": [
        "Like N-channel but reversed.",
        "Voltage controls channel.",
        "Analog signal applications."
    ],
    "IGBT_N_Channel": [
        "Combines MOSFET & BJT.",
        "High efficiency switching.",
        "Used in power electronics."
    ],
    "IGBT_P_Channel": [
        "Rare variant of IGBT.",
        "Positive gate control.",
        "Similar use as N-type."
    ],
    "SCR": [
        "Silicon Controlled Rectifier.",
        "Triggered diode switch.",
        "Used in power control."
    ],
    "Triac": [
        "Bidirectional SCR.",
        "Used in AC control.",
        "Triggers on both cycles."
    ],
    "DC_Motor": [
        "Rotates with DC power.",
        "Speed controlled by voltage.",
        "Used in robotics."
    ],
    "AC_Motor": [
        "Runs on AC power.",
        "Reliable and efficient.",
        "Used in appliances."
    ],
    "Three_Phase_Motor_Delta": [
        "Delta-wired AC motor.",
        "High power application.",
        "Industrial machinery."
    ],
    "Three_Phase_Motor_Star": [
        "Star-wired AC motor.",
        "Lower startup current.",
        "Used in automation."
    ],
    "Volt_Meter": [
        "Measures voltage.",
        "Connects in parallel.",
        "Analog or digital."
    ],
    "Current_Meter": [
        "Measures current.",
        "Connects in series.",
        "Also called ammeter."
    ],
    "Ohm_Meter": [
        "Measures resistance.",
        "Uses internal battery.",
        "Part of multimeter."
    ],
    "Power_Meter": [
        "Measures power usage.",
        "Displays watts.",
        "Used in energy audits."
    ],
    "Fuse": [
        "Overcurrent protection.",
        "Melts when overloaded.",
        "One-time protection."
    ],
    "Normally_Open_Relay": [
        "Electromagnetic switch.",
        "Closes when energized.",
        "Used for automation."
    ],
    "SPS_Open": [
        "Single pole switch open.",
        "Breaks one connection.",
        "Manual or automated."
    ],
    "DPST_Open": [
        "Double pole switch open.",
        "Breaks two circuits.",
        "Used in mains switching."
    ],
    "TPST_Open": [
        "Triple pole switch open.",
        "Three independent contacts.",
        "Used in 3-phase systems."
    ],
    "SPST": [
        "Single Pole Single Throw.",
        "Basic on/off switch.",
        "Used in simple circuits."
    ],
    "DPST": [
        "Double Pole Single Throw.",
        "Switches two lines together.",
        "Isolates both wires."
    ],
    "Teleruptor": [
        "Pulse-controlled switch.",
        "Used in stairwell lighting.",
        "Maintains state after pulse."
    ],
    "Three_Way_Switch": [
        "Controls light from two locations.",
        "Used in staircases.",
        "Has three terminals."
    ],
    "Four_Way_Switch": [
        "Works with 3-way switches.",
        "Controls light from 3+ locations.",
        "Intermediate switch."
    ],
    "Staircase_Timer_Auto": [
        "Automatic delay-off timer.",
        "Common in stairwell lights.",
        "Saves energy."
    ],
    "Circuit_Breaker": [
        "Resettable overcurrent protection.",
        "Trips on fault.",
        "Safer than fuses."
    ],
    "Transformer": [
        "Transfers AC power between circuits.",
        "Steps voltage up/down.",
        "Uses electromagnetic induction."
    ],
    "Ground": [
        "Reference voltage point.",
        "Safety connection.",
        "Used in all circuits."
    ]
}

componentsMenu = [
    "Resistors",
    "Capacitors",
    "Diodes",
    "Residential",
    "Residential_2",
    "Powersources",
    "Grounds",
    "Inductors",
    "Meters",
    "Motors",
    "Transistors",
    "Thyristors",
    "Transformers",
    "CommentBlock",
]

CommentBlock = [
     ("feedbackBlock", load_and_scale_image("./images/feedback.png", 40, 40))
]
# Image names (used for resistors dropdown)
Resistors = [
    ("Resistor", load_and_scale_image("./images/Resistor.png", 80, 40)),
    ("Varistor", load_and_scale_image("./images/Varistor.png", 80, 40)),
    ("Thermistor", load_and_scale_image("./images/Thermistor.png", 80, 40)),
    ("LDR", load_and_scale_image("./images/LDR.png", 80, 40)),
    ("Potentiometer", load_and_scale_image("./images/Potentiometer.png", 80, 40)),
]


Capacitors = [
    ("Capacitor", load_and_scale_image("./images/Capacitor.png", 80, 40)),
     ("Var. Capacitor", load_and_scale_image("./images/Variable_capacitor.png", 80, 40)),
     ("Polar. Capacitor", load_and_scale_image("./images/Polarized_capacitor.png", 80, 40)),
     ("Var. Polar. Capacitor", load_and_scale_image("./images/Variable_polarized_capacitor.png", 80, 40)),
]

Diodes = [
    ("Diode", load_and_scale_image("./images/Diode.png", 80, 40)),
     ("Schottky Diode", load_and_scale_image("./images/Schottky_diode.png", 80, 40)),
     ("Zener Diode", load_and_scale_image("./images/Zener_diode.png", 80, 40)),
     ("LED", load_and_scale_image("./images/LED.png", 80, 40)),
    ("Photo_Diode", load_and_scale_image("./images/Photo_Diode.png", 80, 40)),
]

Inductors = [
    ("Inductor", load_and_scale_image("./images/Inductor.png", 80, 40)),
     ("Var. Inductor", load_and_scale_image("./images/Variable_inductor.png", 80, 40)),
]

Powersources = [
    ("Battery", load_and_scale_image("./images/Battery.png", 80, 40)),
    ("DC Voltage Src", load_and_scale_image("./images/DC_voltage_source.png", 80, 40)),
    ("AC Voltage Src", load_and_scale_image("./images/AC_voltage_source.png", 80, 40)),
    ("Three Phase Power Src", load_and_scale_image("./images/Three_Phase_Power_Src.png", 80, 40)),
]

Transistors = [
    ("NPN Transistor", load_and_scale_image("./images/NPN_transistor.png", 80, 40)),
    ("PNP Transistor", load_and_scale_image("./images/PNP_transistor.png", 80, 40)),
    ("MOSFET N Depl.", load_and_scale_image("./images/MOSFET_N_channel_depletion_type.png", 80, 40)),
    ("MOSFET N Enhance.", load_and_scale_image("./images/MOSFET_N_channel_enhancement_type.png", 80, 40)),
    ("MOSFET P Depl.", load_and_scale_image("./images/MOSFET_P_channel_depletion_type.png", 80, 40)),
    ("MOSFET P Enhance.", load_and_scale_image("./images/MOSFET_P_channel_enhancement_type.png", 80, 40)),
    ("JFET N Channel", load_and_scale_image("./images/JFET_N_channel.png", 80, 40)),
    ("JFET P Channel", load_and_scale_image("./images/JFET_P_channel.png", 80, 40)),
    ("IGBT N Channel", load_and_scale_image("./images/IGBT_N_channel.png", 80, 40)),
    ("IGBT P Channel", load_and_scale_image("./images/IGBT_P_channel.png", 80, 40)),
]

Thyristors = [
    ("SCR", load_and_scale_image("./images/SCR.png", 80, 40)),
    ("Triac", load_and_scale_image("./images/Triac.png", 80, 40)),
]

Motors = [
    ("DC Motor", load_and_scale_image("./images/DC_motor.png", 80, 40)),
    ("AC Motor", load_and_scale_image("./images/AC_motor.png", 80, 40)),
    ("Three Phase Motor Delta", load_and_scale_image("./images/Three_Phase_Motor_Delta.png", 80, 40)),
    ("Three Phase Motor Star", load_and_scale_image("./images/Three_Phase_Motor_Star.png", 80, 40)),
]

Meters = [
    ("Volt Meter", load_and_scale_image("./images/Volt_meter.png", 80, 40)),
    ("Current Meter", load_and_scale_image("./images/Current_meter.png", 80, 40)),
    ("Ohm Meter", load_and_scale_image("./images/Ohm_Meter.png", 80, 40)),
    ("Power Meter", load_and_scale_image("./images/Power_Meter.png", 80, 40)),
]

Residential_2 = [
    ("Fuse", load_and_scale_image("./images/Fuse.png", 80, 40)),
    ("Socket", load_and_scale_image("./images/Socket.png", 40, 40)),
    ("Lamp", load_and_scale_image("./images/Lamp.png", 80, 40)),
]

Residential = [
    ("Normally Open Relay", load_and_scale_image("./images/Relay_open.png", 80, 40)),
    ("SPS Open", load_and_scale_image("./images/switches/SPS_Open.png", 80, 40)),
    ("DPST Open", load_and_scale_image("./images/switches/DPST_Open.png", 80, 40)),
    ("TPST Open", load_and_scale_image("./images/switches/TPST_Open.png", 80, 40)),
    ("SPST", load_and_scale_image("./images/switches/SPST.png", 80, 40)),
    ("DPST", load_and_scale_image("./images/switches/DPST.png", 80, 40)),
    ("Teleruptor", load_and_scale_image("./images/switches/Teleruptor.png", 80, 40)),
    ("Three Way Switch", load_and_scale_image("./images/switches/3_Way_Switch.png", 80, 40)),
    ("Four Way Switch", load_and_scale_image("./images/switches/4_Way_Switch.png", 80, 40)),
    ("Staircase Timer Auto", load_and_scale_image("./images/switches/Staircase_Timer_Auto.png", 80, 40)),
    ("Circuit_Breaker", load_and_scale_image("./images/switches/Circuit_Breaker_On.png", 80, 40)),
]

Transformers = [
    ("Transformer", load_and_scale_image("./images/Transformator.png", 80, 40)),
]

Grounds = [
    ("Ground", load_and_scale_image("./images/Ground.png", 80, 40)),
]

# Load the component menu image and scale it smoothly
menu_background = pygame.image.load("./images/menus/componentmenu.png")
menu_background = pygame.transform.smoothscale(menu_background, (300, 560))

# Font for components and other text

# Text for "Components" title
componentTitle = font4.render("Components", True, BLUETEXT)
title2 = componentTitle.get_rect(topleft=(20, 150))
saved_component_text = font2.render("Saved components", True, WHITE)

# Dropdown menu variables
componentDropdown_visible = False
saved_components_Dropdown_visible = False
dropdown_timer = None
dropdown_border_rect = None
menu = None
nameForClass = None
scroll_offset = 0

component_colors = {component: WHITE for component in componentsMenu}
saved_component_text_color = WHITE  # Initial color for "Saved components" text

dropdown_x = 210
dropdown_y = 200

cross_img = pygame.image.load("./images/icons/cross.png")
cross_img = pygame.transform.smoothscale(cross_img, (8, 8))

def componentMenus(event, mouse_pos, screen, ui_height, adding_comp, selected_comps_wires, dragged_comp, virtual_selecting_box, menu_is_open, hand_cursor):
    global componentDropdown_visible, saved_components_Dropdown_visible, dropdown_timer, dropdown_border_rect, menu, nameForClass, saved_component_text_color, scroll_offset, dropdown_x, dropdown_y, saved_components
    selected_saved_comp = None
    # Titles and their positions
    saved_component_text_rect = saved_component_text.get_rect(topleft=(20, ui_height))

    # Highlight "Saved components" text on hover or if the dropdown is visible
    if saved_component_text_rect.collidepoint(mouse_pos) or saved_components_Dropdown_visible:
        saved_component_text_color = HIGHLIGHT_TEXT_COLOR
        selected_font = font3
    else:
        saved_component_text_color = WHITE
        selected_font = font2

    # Draw titles


    screen.blit(componentTitle, title2)
    highlighted_saved_text = selected_font.render("Saved components", True, saved_component_text_color)
    screen.blit(highlighted_saved_text, saved_component_text_rect)

    # Vertical starting position
    textPlace = 200
    current_hovered_component = None  # Track the currently hovered component

    # Close other menus when "Saved components" menu is open
    if saved_component_text_rect.collidepoint(mouse_pos):
        saved_components_Dropdown_visible = True
        componentDropdown_visible = False
        dropdown_timer = pygame.time.get_ticks()

    # If the dropdown menu is visible, draw it
    
    if saved_components_Dropdown_visible and not adding_comp and not selected_comps_wires and not dragged_comp and not virtual_selecting_box and not menu_is_open:

        if event.type == pygame.MOUSEWHEEL:

            if event.y > 0:  # Scroll up
                dropdown_y += event.y * 25
                event.y = 0
            elif event.y < 0:  # Scroll down
                dropdown_y += event.y * 25
                event.y = 0

        # Background for the dropdown menu
        saved_components_menu_background = pygame.image.load("./images/menus/saved_components_menu.png")
        saved_components_menu_background = pygame.transform.smoothscale(saved_components_menu_background, (900, 50))

        # First draw the standard 2 placeholder backgrounds
        for i in range(10):  # Always draw 2 placeholders
            img_y = dropdown_y + 25 + (50 * i)  # Y position for placeholder background
            dropdown_item_rect = pygame.Rect(dropdown_x, dropdown_y + (50 * i), 900, 50)
            screen.blit(saved_components_menu_background, dropdown_item_rect)  # Draw placeholder background

        # Now calculate how many additional backgrounds are needed if there are more than 3 components
        num_extra_backgrounds = max(0, len(saved_components) - 3)  # Extra backgrounds if there are more than 3 components

        # Render extra backgrounds for additional components beyond the first 3
        for i in range(num_extra_backgrounds):
            img_y = dropdown_y + 25 + (50 * (i + 2))  # Y position for extra background after the first 2
            dropdown_item_rect = pygame.Rect(dropdown_x, dropdown_y + (50 * (i + 2)), 900, 50)
            screen.blit(saved_components_menu_background, dropdown_item_rect)  # Draw extra background

        # Render the saved components and their details
        cross_rects = []  # Store cross rects for click detection
        for i, comp in enumerate(saved_components[:3 + num_extra_backgrounds]):  # Only render up to the max backgrounds needed
            img_y = dropdown_y + 25 + (50 * i)  # Y position for each component in the dropdown
            name_y = dropdown_y + 20 + (50 * i)  # Name Y position for each component

            # Define the rectangle area for each dropdown item
            dropdown_item_rect = pygame.Rect(dropdown_x + 20, dropdown_y + (50 * i), 880, 50)
            dropdown_item_full_rect = pygame.Rect(dropdown_x, dropdown_y + (50 * i), 900, 50)

            # Draw cross icon and store its rect for click detection
            cross_x = dropdown_x + 5
            cross_y = dropdown_y + 3 + (50 * i)
            cross_rect = pygame.Rect(cross_x, cross_y, 8, 8)
            screen.blit(cross_img, (cross_x, cross_y))
            cross_rects.append((cross_rect, i))

            # Check if the mouse is hovering over this dropdown item

            if dropdown_item_full_rect.collidepoint(mouse_pos):
                dropdown_timer = pygame.time.get_ticks()
            if dropdown_item_rect.collidepoint(mouse_pos):
                # Highlight the component name text when hovered
                component_name_text = font2.render(comp.__class__.__name__, True, HIGHLIGHT_TEXT_COLOR)  # Highlight color for hovered item
                selected_saved_comp = comp
                dropdown_timer = pygame.time.get_ticks()
            else:
                # Default color for the component name text
                component_name_text = font.render(comp.__class__.__name__, True, WHITE)

            # Draw the dropdown item background (rectangle)
            

            # Load and scale component image
            image = load_and_scale_image(comp.image_path, 80, 40)
            screen.blit(image, (dropdown_x + (100 / 2) - (image.get_width() / 2), img_y - (image.get_height() / 2)))

            # Get the component name and render it
            name_x = dropdown_x + 105
            screen.blit(component_name_text, (name_x, name_y))

            # Render the properties for the component horizontally
            prop_x = dropdown_x + 300  # Starting X position for properties
            for prop_name, value in comp.properties:
                # Render property name
                prop_name_text = font.render(f"{prop_name}:", True, WHITE)
                screen.blit(prop_name_text, (prop_x, name_y))

                # Render property value
                prop_name_width = prop_name_text.get_width()
                prop_value_text = font.render(str(value), True, WHITE)
                screen.blit(prop_value_text, (prop_x + prop_name_width + 5, name_y))  # 5px after the property name

                # Update `prop_x` for the next property
                prop_x += prop_name_width + prop_value_text.get_width() + 15  # Add spacing between properties

        # Handle cross click event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for cross_rect, idx in cross_rects:
                if cross_rect.collidepoint(mouse_pos):
                    if idx < len(saved_components):
                        del saved_components[idx]
                        break  # Only delete one per click

    # Loop through componentsMenu
    for componentText in componentsMenu:
        # Use font if the component is highlighted, otherwise use font
        current_font = font3 if component_colors[componentText] == HIGHLIGHT_TEXT_COLOR else font2
        text_surface = current_font.render(componentText, True, component_colors[componentText])
        text_rect = text_surface.get_rect(topleft=(20, textPlace))
        screen.blit(text_surface, text_rect)

        # Hover logic
        if text_rect.collidepoint(mouse_pos):
            current_hovered_component = componentText  # Track the hovered component
            component_colors[componentText] = HIGHLIGHT_TEXT_COLOR
            componentDropdown_visible = True
            saved_components_Dropdown_visible = False  # Close "Saved components" menu
            dropdown_timer = pygame.time.get_ticks()
            menu = globals()[componentText]  # Assign the corresponding menu

        textPlace += 40

    # Reset non-hovered components to white only when the menu is closed
    if not componentDropdown_visible:
        for componentText in componentsMenu:
            component_colors[componentText] = WHITE

    # Draw dropdown menu
    if componentDropdown_visible and not adding_comp and not selected_comps_wires and not dragged_comp and not virtual_selecting_box and not menu_is_open:
        menu_rect = pygame.Rect(dropdown_x, dropdown_y, menu_background.get_width(), menu_background.get_height())
        screen.blit(menu_background, (dropdown_x, dropdown_y))
        dropdown_border_rect = menu_rect

        # Reset timer when hovering over dropdown
        if menu_rect.collidepoint(mouse_pos):
            dropdown_timer = pygame.time.get_ticks()

        nameForClass = None

        if menu:
            for i, (name, img) in enumerate(menu):
                name_y = dropdown_y + 22 + (51 * i)
                img_y = dropdown_y + (50 * i)
                screen.blit(img, (dropdown_x + (100 / 2) - (img.get_width() / 2), name_y - 15))

                # Highlight logic
                name_text_color = WHITE
                img_rect = pygame.Rect(dropdown_x, img_y, 300, 50)
                name_text_font = font
                if img_rect.collidepoint(mouse_pos):
                    name_text_color = HIGHLIGHT_TEXT_COLOR
                    name_text_font = font2
                    nameForClass = name.replace(" ", "_").replace(".", "")
                    draw_component_info(nameForClass)
                # Use the default font for dropdown menu text
                name_text = name_text_font.render(name, True, name_text_color)
                screen.blit(name_text, (dropdown_x + 105, name_y))
                
                    
    # Hide dropdown when timer expires
    if dropdown_timer:
        if pygame.time.get_ticks() - dropdown_timer > DROPDOWN_DELAY or adding_comp:
            componentDropdown_visible = False
            saved_components_Dropdown_visible = False
            dropdown_timer = None
            nameForClass = None
            dropdown_y = 200
    # Ensure the highlighted component text remains highlighted
    if current_hovered_component:
        for componentText in componentsMenu:
            if componentText != current_hovered_component:
                component_colors[componentText] = WHITE
    
    if nameForClass or selected_saved_comp:
        hand_cursor = True

    return nameForClass, selected_saved_comp, hand_cursor

def save_component(saved_comp):
    global saved_components
    print(saved_components)
    # Add the saved component to the saved_components list
    saved_components.append(saved_comp)

def draw_component_info(nameForClass):
    if nameForClass not in component_explanations:
        return  # Component not recognized

    # Dimensions and positioning
    rect_width, rect_height = 300, 200
    info_rect = pygame.Rect(0, 0, rect_width, rect_height)
    info_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Draw background
    pygame.draw.rect(screen, DARKBLUE, info_rect, border_radius=5)

    # Display text
 
    explanations = component_explanations[nameForClass]
    for i, line in enumerate(explanations):
        rendered = font2.render(line, True, WHITE)
        text_pos = (info_rect.x + 20, info_rect.y + 20 + i * 30)
        screen.blit(rendered, text_pos)