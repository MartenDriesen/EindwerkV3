from main.global_constants import SCREEN_HEIGHT, SCREEN_WIDTH, screen, font2, WHITE, DARKBLUE
import pygame

def shortcuts(mouse_pos):
    # --- Render "shortcuts" text ---
    save_text = font2.render("shortcuts", True, WHITE)
    save_rect = save_text.get_rect(topleft=(15, SCREEN_HEIGHT - 80))  # tightly fit text

    # --- Blit text ---
    screen.blit(save_text, save_rect)

    # --- Hover check ---
    if save_rect.collidepoint(mouse_pos):
        # Draw info panel
        panel_width, panel_height = 400, 400
        panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
        panel_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.draw.rect(screen, DARKBLUE, panel_rect, border_radius=5)

        # Display shortcut text
        shortcuts_list = [
            "Ctrl + S: Save",
            "Ctrl + Z: Undo",
            "Ctrl + shift + Z: Redo",
            "Delete: Delete (delete selected component)", 
            "Ctrl + C: Copy",
            "Ctrl + V: Paste",
            "hold shift to drag camera",
            "Ctrl + scroll: zoom in/out",
        ]

        text_y = panel_rect.y + 20
        for line in shortcuts_list:
            text_surface = font2.render(line, True, WHITE)
            screen.blit(text_surface, (panel_rect.x + 20, text_y))
            text_y += text_surface.get_height() + 10
