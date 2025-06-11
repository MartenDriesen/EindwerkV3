import pygame
from main.global_constants import font, screen, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, LIGHT_BLUE

component = None
active_field = None
first_input = True
menu_is_open = False
border_draw_time = None
time_for_red_box = 0
input_selected = None
def properties_menu(new_component, left_mouse_button, mouse_pos, event, hand_cursor):
    global component, active_field, first_input, menu_is_open, border_draw_time, time_for_red_box
    global active_field, input_selected
    menu_is_open = True
    component = new_component
    mouse_x, mouse_y = mouse_pos

    # Load and scale the menu background
    properties_menu_image = pygame.image.load("./images/menus/properties.png")
    properties_menu_image = pygame.transform.smoothscale(properties_menu_image, (350, 245))

    if not input_selected:
        active_field = component.properties[0][0]
        input_selected = True
    # Text strings
    place = "Place"
    place_and_save_component = "Place & Save Component"

    # Render text
    place_text = font.render(place, True, WHITE)
    place_and_save_component_text = font.render(place_and_save_component, True, WHITE)

    # Display the component's class name
    component_name = component.__class__.__name__  # Dynamically fetch the class name
    component_name_text = font.render(component_name, True, WHITE)
    component_name_text_rect = component_name_text.get_rect(center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100))

    # Create the menu rect and center it
    properties_menu_rect = properties_menu_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # Define button rectangles to align with the text
    button_padding = 5
    place_text_rect = font.render(place, True, WHITE).get_rect(center=((SCREEN_WIDTH / 2) + 120, (SCREEN_HEIGHT / 2) + 95))
    place_text_button_rect = place_text_rect.inflate(button_padding * 2, button_padding * 2)

    place_and_save_component_text_rect = font.render(place_and_save_component, True, WHITE).get_rect(
        center=((SCREEN_WIDTH / 2) - 55, (SCREEN_HEIGHT / 2) + 95)
    )
    place_and_save_component_button_rect = place_and_save_component_text_rect.inflate(button_padding * 2, button_padding * 2)

    # Red rectangle logic
    draw_red_rect = False
    if event:
        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
            component.edited = True
            menu_is_open = False
            print("event")
            return 1, hand_cursor  # Close the menu and place the component

    if time_for_red_box == 0:
        time_for_red_box = pygame.time.get_ticks()
 

    if not properties_menu_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button and pygame.time.get_ticks() - time_for_red_box >= 300:
            # Clicked outside the menu

        draw_red_rect = True
        border_draw_time = pygame.time.get_ticks()  # Record the current time
        
            # Check if "Place" button is clicked
    if (place_text_button_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button):
        component.edited = True
        menu_is_open = False
        print("placed")
        time_for_red_box = 0
        return 1, hand_cursor  # Close the menu and place the component

            # Check if "Place & Save Component" button is clicked
    if place_and_save_component_button_rect.collidepoint(mouse_x, mouse_y) and left_mouse_button:
        component.edited = True
        menu_is_open = False
        time_for_red_box = 0
        print(component)
        print("saved")
        return component, hand_cursor  # Close the menu and save the component
    
    if border_draw_time:
        # Render red rectangle behind the menu if needed
        if draw_red_rect or (pygame.time.get_ticks() - border_draw_time <= 1000):  # Show for 1 second
            pygame.draw.rect(screen, RED, properties_menu_rect)

    # Render menu background
    screen.blit(properties_menu_image, properties_menu_rect)

    # Draw light blue buttons directly behind the text
    pygame.draw.rect(screen, LIGHT_BLUE, place_text_button_rect, border_radius=5)
    pygame.draw.rect(screen, LIGHT_BLUE, place_and_save_component_button_rect, border_radius=5)

    # Render text on top of buttons
    screen.blit(place_text, place_text_rect)
    screen.blit(place_and_save_component_text, place_and_save_component_text_rect)
    screen.blit(component_name_text, component_name_text_rect)
    
    input_fields = []
    # Set the first input field to active if first_input is True
    
      # Set active_field to the name of the first property


    for i, (prop_name, value) in enumerate(component.properties):
    # Determine the column (0 for left, 1 for right) and row
        column = i % 2  # 0 for left, 1 for right
        row = i // 2    # Row index
    
    # Calculate the x and y positions for the input fields
        x_offset = (SCREEN_WIDTH / 2) - 125 + (column * 150)  # 150px between columns
        y_offset = (SCREEN_HEIGHT / 2) - 80 + row * 40      # 40px between rows

    # Create the input field rect
        input_field_rect = pygame.Rect(0, 0, 55, 22)  # Width 50, height 22
        input_field_rect.topleft = (x_offset, y_offset)  # Position rect at calculated offset
        input_fields.append((input_field_rect, prop_name))

    # Determine border color
        border_color = LIGHT_BLUE if active_field == prop_name else WHITE

    # Render the input field
        pygame.draw.rect(screen, (255, 255, 255), input_field_rect)  # Fill the input field with white
        pygame.draw.rect(screen, border_color, input_field_rect, 2)  # Draw border

    # Render the property name 5px to the right of the input field
        prop_text = font.render(prop_name, True, WHITE)
        prop_text_rect = prop_text.get_rect(midleft=(input_field_rect.right + 5, input_field_rect.centery))
        screen.blit(prop_text, prop_text_rect)

    # Render the value inside the input field as the placeholder text
        input_value = str(value) if value != 0 else "0"  # Show the current property value or "0"
        input_value_text = font.render(input_value, True, BLACK)
        screen.blit(input_value_text, (input_field_rect.x + 5, input_field_rect.y + 5))

    # Handle events
    if left_mouse_button:  # Left mouse button
        for rect, prop_name in input_fields:
            if rect.collidepoint(mouse_x, mouse_y):
                # Before switching to the new field, check if the current active field is empty
                for i, (prop_name_in_list, value) in enumerate(component.properties):
                    if prop_name_in_list == active_field and value == "":  # If the active field is empty
                        component.properties[i][1] = "0"  # Set to "0" before switching
                        print(f"Field {prop_name_in_list} was empty, set to default value 0")
                    
                    # Now switch to the new active field
                active_field = prop_name
                print(f"Active field set to: {prop_name}")
                break

    for rect, prop_name in input_fields:
        if rect.collidepoint(mouse_x, mouse_y):
            # Before switching to the new field, check if the current active field is empty
            for i, (prop_name_in_list, value) in enumerate(component.properties):
                if prop_name_in_list == active_field:
                    if value == "":  # If the active field is empty, set it to "0" immediately
                        component.properties[i][1] = "0"  # Set to "0" before switching
                        print(f"Field {prop_name_in_list} was empty, set to default value 0")

            # Now switch to the new active field
            active_field = prop_name
            print(f"Active field set to: {prop_name}")
            break

    # Handling event for digit input
    if event:
        if event.type == pygame.KEYDOWN and active_field:
            # Get the index of the active field in component properties
            for i, (prop_name_in_list, value) in enumerate(component.properties):
                if prop_name_in_list == active_field:
                    # Convert the value to string before checking length
                    value_str = str(value)
                    
                    if event.unicode.isdigit():  # Check if the key pressed is a digit
                        # Only allow input if the value has less than 6 digits
                        if len(value_str) < 6:
                            # If the value is "0", replace it with the typed digit
                            if value_str == "0":
                                component.properties[i][1] = event.unicode  # Set the typed value directly
                            else:
                                # If it's not "0", append the typed digit to the existing value
                                component.properties[i][1] = value_str + event.unicode  # Append the digit
                            print(f"Updated {prop_name_in_list} to {component.properties[i][1]}")
                    elif event.key == pygame.K_BACKSPACE:
                        # Handle backspace to delete a character from the value
                        new_value = value_str[:-1] if value_str != "0" else ""  # Remove last character unless it's "0"
                        component.properties[i][1] = new_value if new_value != "" else "0"  # Ensure it doesn't become empty
                        print(f"Updated {prop_name_in_list} to {new_value}")

    # Immediately handle the empty field update while rendering
    for i, (prop_name, value) in enumerate(component.properties):
        value_str = str(value)
        # Ensure that the field is set to "0" if it's empty and active
        if value_str == "" and prop_name == active_field:
            component.properties[i][1] = "0"  # Ensure that any empty field is immediately set to 0

    # Handle Tab key press for switching fields
    if event and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_TAB and active_field:
            # Find the index of the currently active field
            active_field_index = None
            for idx, (prop_name, _) in enumerate(component.properties):
                if prop_name == active_field:
                    active_field_index = idx
                    break
            
            # If the Tab key is pressed, cycle to the next field
            if active_field_index is not None:
                # Move to the next input field
                next_index = (active_field_index + 1) % len(component.properties)  # Loop back to the first field if at the end
                active_field = component.properties[next_index][0]  # Update active field to the next one
                print(f"Switched to next field: {active_field}")
    
    if place_text_button_rect.collidepoint(mouse_x, mouse_y) or place_and_save_component_button_rect.collidepoint(mouse_x, mouse_y):
        hand_cursor = True
    return None, hand_cursor
def is_property_menu_open():
    return menu_is_open