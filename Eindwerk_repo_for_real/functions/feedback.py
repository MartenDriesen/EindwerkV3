import pygame
from main.global_constants import screen, SCREEN_WIDTH, SCREEN_HEIGHT, font2, font5

# Global state
feedback_checkbox_checked = False
show_feedback_panel = False
feedback_input_active = False
feedback_text_input = ""
current_feedback_comp = None

# UI constants
CHECKBOX_SIZE = 20
CHECKBOX_POS = (15, SCREEN_HEIGHT - 110)
INPUT_BOX_SIZE = (300, 30)

BLUE = pygame.Color("#0199FF")
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")

def draw_checkbox(screen, checked):
    x, y = CHECKBOX_POS
    pygame.draw.rect(screen, WHITE, (x, y, CHECKBOX_SIZE, CHECKBOX_SIZE))
    if checked:
        padding = 5
        pygame.draw.rect(screen, BLUE, (x + padding, y + padding, CHECKBOX_SIZE - 2*padding, CHECKBOX_SIZE - 2*padding))

def handle_checkbox_click(mouse_pos):
    global feedback_checkbox_checked
    x, y = CHECKBOX_POS
    checkbox_rect = pygame.Rect(x, y, CHECKBOX_SIZE, CHECKBOX_SIZE)
    if checkbox_rect.collidepoint(mouse_pos):
        feedback_checkbox_checked = not feedback_checkbox_checked

def draw_input_box(screen, hovered_comp, event, mouse_pos, left_mouse_button):
    global feedback_input_active, feedback_text_input, show_feedback_panel

    panel_width = 320
    panel_rect = pygame.Rect(SCREEN_WIDTH - panel_width, 0, panel_width, SCREEN_HEIGHT)
    pygame.draw.rect(screen, WHITE, panel_rect)
    pygame.draw.rect(screen, (0, 31, 56), panel_rect, 4)

    # Instruction
    instruction = font2.render("Click in the box to add feedback.", True, BLACK)
    screen.blit(instruction, (panel_rect.x + 10, panel_rect.y + 10))

    # Close Button
    cross_img = pygame.image.load("./images/icons/Bluecross.png")
    cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
    cross_rect = cross_img.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(cross_img, cross_rect)

    if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
        show_feedback_panel = False
        feedback_input_active = False
        if hovered_comp:
            hovered_comp.feedback = feedback_text_input
        return

    # Input Box
    input_box_height = 1000
    input_box = pygame.Rect(panel_rect.x + 10, panel_rect.y + 40, panel_width - 20, input_box_height)
    input_bg_color = (230, 230, 230) if not feedback_input_active else (210, 210, 210)
    pygame.draw.rect(screen, input_bg_color, input_box)
    pygame.draw.rect(screen, (0, 31, 56), input_box, 2)

    # Click to activate
    if panel_rect.collidepoint(mouse_pos) and left_mouse_button:
        feedback_input_active = True

    # Typing input
    if feedback_input_active and event and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            feedback_text_input = feedback_text_input[:-1]
        elif event.key == pygame.K_RETURN:
            feedback_text_input += "\n"
        elif len(feedback_text_input) < 1000:
            feedback_text_input += event.unicode

    # Text Wrapping
    line_chars = 40
    lines = []
    text = feedback_text_input
    while len(text) > line_chars:
        lines.append(text[:line_chars])
        text = text[line_chars:]
    lines.append(text)

    y_offset = 0
    for line in lines:
        rendered = font2.render(line, True, BLACK)
        screen.blit(rendered, (input_box.x + 5, input_box.y + 5 + y_offset))
        y_offset += rendered.get_height() + 2

def get_feedback(components, virtual_mouse_pos, dragged_component, selected_comps_wires, drawing_line, left_mouse_button, event):
    global show_feedback_panel, feedback_checkbox_checked
    global feedback_input_active, feedback_text_input, current_feedback_comp

    # Draw checkbox + label

    label = font5.render("Show feedback:", True, (255, 255, 255))
    screen.blit(label, (CHECKBOX_POS[0] + CHECKBOX_SIZE + 10, CHECKBOX_POS[1]))
    draw_checkbox(screen, feedback_checkbox_checked)

    # Check for checkbox toggle
    if left_mouse_button:
        handle_checkbox_click(virtual_mouse_pos)

    # Identify hovered component
    hovered_comp = None
    for comp in components:
        if comp.rotation in [90, 270]:
            rect = pygame.Rect(comp.x, comp.y, comp.size_y, comp.size_x)
        else:
            rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)

        if rect.collidepoint(virtual_mouse_pos):
            if not dragged_component and not selected_comps_wires and not drawing_line:
                if hasattr(comp, 'feedback'):
                    hovered_comp = comp
                    break

    # Update state based on checkbox and hover
    if feedback_checkbox_checked and hovered_comp:
        if current_feedback_comp != hovered_comp:
            feedback_input_active = False  # Reset input state when switching
        show_feedback_panel = True
        current_feedback_comp = hovered_comp
        feedback_text_input = hovered_comp.feedback
    elif not feedback_checkbox_checked:
        show_feedback_panel = False
        feedback_input_active = False
        current_feedback_comp = None

    # Draw feedback panel
    if show_feedback_panel and current_feedback_comp:
        
        draw_input_box(screen, current_feedback_comp, event, virtual_mouse_pos, left_mouse_button)

        # Update feedback back into the component
        if event:
            current_feedback_comp.feedback = feedback_text_input
