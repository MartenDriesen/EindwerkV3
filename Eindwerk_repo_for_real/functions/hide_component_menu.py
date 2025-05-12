import pygame
from main.global_constants import SCREEN_HEIGHT, WHITE, screen, LIGHT_BLUE

hide_font = pygame.font.Font(None, 26)

hide_component_menu_text = hide_font.render("<< hide menu", True, WHITE)
show_component_menu_text = hide_font.render(">> show menu", True, WHITE)

hide_component_menu_rect = pygame.Rect(10, SCREEN_HEIGHT - 40, 130, 30)
hide_component_menu_rect_text = hide_component_menu_text.get_rect(topleft=(21, SCREEN_HEIGHT - 32))  

def hide_component_menu(mouse_pos, left_mouse_button, hide_menu, hand_cursor):

   if hide_component_menu_rect.collidepoint(mouse_pos):
      hand_cursor = True
      if left_mouse_button:                 
         if not hide_menu:
            hide_menu = True
         else:
             hide_menu = False   

   pygame.draw.rect(screen, LIGHT_BLUE, hide_component_menu_rect, 0, border_radius = 5)  

   if not hide_menu:
      screen.blit(hide_component_menu_text, hide_component_menu_rect_text)
   else:
      screen.blit(show_component_menu_text, hide_component_menu_rect_text) 

   return hide_menu, hand_cursor                       
