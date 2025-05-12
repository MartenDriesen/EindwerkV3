import pygame
from main.global_constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, font, screen

feedback_panel_open = False
feedback_input_active = False
feedback_text_input = ""

def feedback(event, mouse_pos, left_mouse_button):
    global feedback_panel_open, feedback_input_active, feedback_text_input

    # --- Load Feedback Icon ---
    feedback_img = pygame.image.load("./images/icons/feedback.png")
    feedback_img = pygame.transform.smoothscale(feedback_img, (30, 25))
    feedback_img_rect = feedback_img.get_rect(center=(SCREEN_WIDTH // 2, 65))
    screen.blit(feedback_img, feedback_img_rect)

    # --- Label ---
    feedback_text = font.render("Feedback", True, WHITE)
    screen.blit(feedback_text, (feedback_img_rect.centerx - feedback_text.get_width() // 2,
                                feedback_img_rect.bottom + 4))

    # --- Toggle Panel ---
    if feedback_img_rect.collidepoint(mouse_pos) and left_mouse_button:
        feedback_panel_open = not feedback_panel_open
        feedback_input_active = False

    feedback_return = None

    if feedback_panel_open:
        panel_width = 280
        panel_rect = pygame.Rect(SCREEN_WIDTH - panel_width, 0, panel_width, SCREEN_HEIGHT)
        pygame.draw.rect(screen, WHITE, panel_rect)
        pygame.draw.rect(screen, (0, 31, 56), panel_rect, 4)

        # --- Instruction ---
        instruction = font.render("Click in white area to add feedback.", True, (0, 0, 0))
        screen.blit(instruction, (panel_rect.x + 10, panel_rect.y + 10))

        # --- Close Button ---
        cross_img = pygame.image.load("./images/icons/Bluecross.png")
        cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
        cross_rect = cross_img.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(cross_img, cross_rect)

        if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
            feedback_panel_open = False
            feedback_input_active = False
            feedback_return = feedback_text_input
            return feedback_text_input

        # --- Input Box (You can control the height here) ---
        input_box_height = 1000
        input_box = pygame.Rect(panel_rect.x + 10, panel_rect.y + 40, panel_width - 20, input_box_height)
        input_bg_color = (230, 230, 230) if not feedback_input_active else (210, 210, 210)
        pygame.draw.rect(screen, input_bg_color, input_box)
        pygame.draw.rect(screen, (0, 31, 56), input_box, 2)

        # --- Activate Typing Anywhere on Panel ---
        if panel_rect.collidepoint(mouse_pos) and left_mouse_button:
            feedback_input_active = True

        # --- Typing ---
        if feedback_input_active and event:
            if event.key == pygame.K_BACKSPACE:
                feedback_text_input = feedback_text_input[:-1]
            elif event.key == pygame.K_RETURN:
                feedback_text_input += "\n"
            elif len(feedback_text_input) < 1000:
                feedback_text_input += event.unicode

        # --- Draw Typed Text (Wrap at ~40 chars) ---
        line_chars = 35
        lines = []
        text = feedback_text_input
        while len(text) > line_chars:
            lines.append(text[:line_chars])
            text = text[line_chars:]
        lines.append(text)  # Add remaining

        y_offset = 0
        for line in lines:
            rendered = font.render(line, True, (0, 0, 0))
            screen.blit(rendered, (input_box.x + 5, input_box.y + 5 + y_offset))
            y_offset += rendered.get_height() + 2

    return feedback_text_input
