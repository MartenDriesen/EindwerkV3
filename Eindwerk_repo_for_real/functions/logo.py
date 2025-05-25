import pygame
from main.global_constants import screen

def logo():
    logo_image = pygame.image.load("./images/logo/icon.png")
    logo_image = pygame.transform.smoothscale(logo_image, (20, 18))
    # Set position: 20px from left, 10px from top
    screen.blit(logo_image, (20, 13))