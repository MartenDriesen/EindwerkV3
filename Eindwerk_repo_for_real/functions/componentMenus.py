import pygame
from main.global_constants import WHITE, HIGHLIGHT_TEXT_COLOR, BLUETEXT, DROPDOWN_DELAY, font, font2, font3, font4
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

componentsMenu = [
    "Resistors",
    "Capacitors",
    "Diodes",
    "Switches",
    "Powersources",
    "Grounds",
    "Inductors",
    "Fuses",
    "Meters",
    "Motors",
    "Transistors",
    "Thyristors",
    "Transformers",
    "CommentBlock",
]

CommentBlock = [
     ("feedbackBlock", load_and_scale_image("./images/feedback.png", 20, 20))
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

Fuses = [
    ("Fuse", load_and_scale_image("./images/Fuse.png", 80, 40)),
]

Switches = [
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

def componentMenus(event, mouse_pos, screen, ui_height, adding_comp, selected_comps_wires, dragged_comp, virtual_selecting_box, menu_is_open, hand_cursor):
    global componentDropdown_visible, saved_components_Dropdown_visible, dropdown_timer, dropdown_border_rect, menu, nameForClass, saved_component_text_color, scroll_offset, dropdown_x, dropdown_y
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
        for i, comp in enumerate(saved_components[:3 + num_extra_backgrounds]):  # Only render up to the max backgrounds needed
            img_y = dropdown_y + 25 + (50 * i)  # Y position for each component in the dropdown
            name_y = dropdown_y + 20 + (50 * i)  # Name Y position for each component

            # Define the rectangle area for each dropdown item
            dropdown_item_rect = pygame.Rect(dropdown_x, dropdown_y + (50 * i), 900, 50)

            # Check if the mouse is hovering over this dropdown item
            if dropdown_item_rect.collidepoint(mouse_pos):
                # Highlight the component name text when hovered
                component_name_text = font2.render(comp.__class__.__name__, True, HIGHLIGHT_TEXT_COLOR)  # Highlight color for hovered item
                selected_saved_comp = comp
                dropdown_timer = pygame.time.get_ticks()
            else:
                # Default color for the component name text
                component_name_text = font.render(comp.__class__.__name__, True, WHITE)

            # Draw the dropdown item background (rectangle)
            screen.blit(saved_components_menu_background, dropdown_item_rect)

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
