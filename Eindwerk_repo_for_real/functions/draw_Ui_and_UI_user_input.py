import pygame
from main.global_constants import font, font4, screen, ui, ui2, uigreen, new_height, new_width2, SCREEN_HEIGHT, SCREEN_WIDTH, LIGHT_BLUE, GREEN, YELLOW, BROWN, RED, BLACK, WHITE
new_width = SCREEN_WIDTH  # The width should be equal to the screen width
new_height2 = SCREEN_HEIGHT

colors = [LIGHT_BLUE, GREEN, YELLOW, BROWN, RED, BLACK]
rectangles = []

x_start = (SCREEN_WIDTH / 2) - 90  # Starting x position
y_start = new_height - 50  # Fixed y position
rect_width, rect_height = 20, 20  # Size of each rectangle
spacing = 30  # Space between rectangles
                   

thermometer_img = pygame.transform.scale(pygame.image.load("./images/icons/thermometer.png"), (13, 25)) 
light_img = pygame.transform.scale(pygame.image.load("./images/icons/light.png"), (30, 30)) 

thermometer_value_rect = pygame.Rect(x_start + 480, y_start , 100, 25)
thermometer_text_rect = pygame.Rect(x_start + 485, y_start + 5 , 100, 25)
light_value_rect = pygame.Rect(x_start + 675, y_start , 100, 25)
light_text_rect = pygame.Rect(x_start + 680, y_start + 5, 100, 25)


wire_color_title = font.render("Wire color", True, WHITE)
wire_color_title_rect = wire_color_title.get_rect(topleft=(x_start + 50, y_start + 30))  

env_temperature_title = font.render("Environment temp <200", True, WHITE)
env_temperature_title_rect = env_temperature_title.get_rect(topleft=(x_start + 460, y_start + 30))  
env_light_title = font.render("Environment light <1000000", True, WHITE)
env_light_title_rect = env_light_title.get_rect(topleft=(x_start + 650, y_start + 30))  




for i in range(len(colors)):
    rect = pygame.Rect(x_start + i * spacing, y_start + 5, rect_width, rect_height)
    rectangles.append(rect)

def draw_Ui(hide_left_menu, is_teacher):
    
    # Calculate the new width to fit the screen width, keeping the aspect ratio
    
    # Scale the image to the new dimensions
    if is_teacher:
        scaled_ui = pygame.transform.smoothscale(uigreen, (new_width, new_height))
    else:
        scaled_ui = pygame.transform.smoothscale(ui, (new_width, new_height))
    # Scale the image to the new dimensions
    scaled_ui2 = pygame.transform.smoothscale(ui2, (new_width2, new_height2))
    if not hide_left_menu:
        screen.blit(scaled_ui2, (0, 0))  # Position it at the top-left corner (0, 0)
    # Draw the scaled image to the screen
    screen.blit(scaled_ui, (0, 0))  # Position it at the top-left corner (0, 0)
    # Draw the scaled image to the screen
    
    for i, rect in enumerate(rectangles):
        if i == selectedRectIndex:
            # Draw a white border for the selected rectangle
            pygame.draw.rect(screen, WHITE, rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(screen, colors[i], rect, border_radius=5)

    screen.blit(wire_color_title, wire_color_title_rect)







selected_wire_color = BLACK
selectedRectIndex = 5

def select_connection_color(mouse_pos, left_mouse_button, adding_comp, hand_cursor):
     
    global selectedRectIndex, selected_wire_color

    if not adding_comp:
        for i, rect in enumerate(rectangles):
            if rect.collidepoint(mouse_pos):
                hand_cursor = True
                if left_mouse_button:
                    selected_wire_color = colors[i]
                    selectedRectIndex = i  # Store the index of the selected rectangle
                break  # Stop checking once a match is found
    return selected_wire_color, hand_cursor



def env_temp_function(mouse_pos, left_mouse_button, envTemp, event, user_input_temp_bool, hand_cursor):

    env_temp_string = str(envTemp)

    if thermometer_value_rect.collidepoint(mouse_pos):
        hand_cursor = True

    if left_mouse_button:
        if thermometer_value_rect.collidepoint(mouse_pos) and not user_input_temp_bool: 
            user_input_temp_bool = True
        else:
            user_input_temp_bool = False
            if env_temp_string == "0":
                env_temp_string = "21"    
    if event:
        if event.key == pygame.K_DELETE:               
            if user_input_temp_bool:  
                env_temp_string = ""    

        elif event.key == pygame.K_BACKSPACE:            
            if user_input_temp_bool:  
                env_temp_string = env_temp_string[:-1]              
            
        elif event.key == pygame.K_RETURN:             
            user_input_temp_bool = False
            if env_temp_string == "0":
                env_temp_string = "21" 

        elif event.unicode.isdigit():  # Allow only numbers
            if user_input_temp_bool and envTemp < 200:  
                env_temp_string += event.unicode

    if env_temp_string == '':  
        env_temp_string = '0'              
    env_temperature = int(env_temp_string) 
    
    if env_temperature > 199:  
        env_temp_string = env_temp_string[:-1] 
        env_temperature = int(env_temp_string)  

    return env_temperature, user_input_temp_bool, hand_cursor


def env_light_function(mouse_pos, left_mouse_button, envLight, event, user_input_light_bool, hand_cursor):  

    env_light_string = str(envLight)
    
    if light_value_rect.collidepoint(mouse_pos):
        hand_cursor = True

    if left_mouse_button:
        if light_value_rect.collidepoint(mouse_pos) and left_mouse_button and not user_input_light_bool: 
            user_input_light_bool = True
        else:
            user_input_light_bool = False  
            if env_light_string == "0":
                env_light_string = "1000" 
    if event and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DELETE:
            if user_input_light_bool:   
                env_light_string = ""     

        elif event.key == pygame.K_BACKSPACE:
            if user_input_light_bool:   
                env_light_string = env_light_string[:-1]            
            
        elif event.key == pygame.K_RETURN:          
            user_input_light_bool = False
            if env_light_string == "0":
                env_light_string = "1000" 

        elif event.unicode.isdigit():  # Allow only numbers
            if user_input_light_bool and envLight < 1000000:   
                env_light_string += event.unicode 
   
    if env_light_string == '':  
        env_light_string = '0'
    env_light = int(env_light_string) 

    if env_light > 999999:  
        env_light_string = env_light_string[:-1] 
        env_light = int(env_light_string)

    return env_light, user_input_light_bool, hand_cursor                 