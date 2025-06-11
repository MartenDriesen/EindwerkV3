from main.global_constants import SCREEN_HEIGHT, SCREEN_WIDTH, screen, font2, WHITE, DARKBLUE
import pygame

def shortcuts(mouse_pos):
    # --- Render "shortcuts" text ---
    shortcuts_text = font2.render("help", True, WHITE)
    shortcuts_rect = shortcuts_text.get_rect(topleft=(500, 12))  # tightly fit text

    # --- Blit text ---
    screen.blit(shortcuts_text, shortcuts_rect)

    # --- Hover check ---
    if shortcuts_rect.collidepoint(mouse_pos):
        # Draw info panel
        panel_width, panel_height = 400, 400
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.draw.rect(screen, DARKBLUE, panel_rect, border_radius=5)

        # Display shortcut text
        shortcuts_list = [
            "Ctrl + M: Open manual",
            "Ctrl + S: Save",
            "Ctrl + Z: Undo",
            "Ctrl + shift + Z: Redo",
            "Delete: delete selected", 
            "Ctrl + C: Copy",
            "Ctrl + V: Paste",
            "hold shift to drag camera",
            "Ctrl + scroll: zoom in/out",
            "Ctrl + A: select all",
            "R: rotate selected",
            "Escape: stop drawing line"
            
        ]

        text_y = panel_rect.y + 20
        for line in shortcuts_list:
            text_surface = font2.render(line, True, WHITE)
            screen.blit(text_surface, (panel_rect.x + 20, text_y))
            text_y += text_surface.get_height() + 10
