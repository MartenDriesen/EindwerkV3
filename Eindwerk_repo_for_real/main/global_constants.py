import pygame

pygame.init()
#pygame.key.set_repeat(500, 50)  # Delay: 500ms, Repeat interval: 50ms
pygame.display.set_caption("Powerlink")
# Screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h 
# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
# ui image
ui = pygame.image.load("./images/menus/ui.png")
ui2 = pygame.image.load("./images/menus/ui2.png")
# get ui size
original_width, original_height = ui.get_size()
original_width2, original_height2 = ui2.get_size()
# get new ui size based on the screen dimensions
new_height = int(original_height * (SCREEN_WIDTH / original_width))
new_width2 = int(original_width2 * (SCREEN_HEIGHT / original_height2))  # Scale the height to maintain aspect ratio
#grid spacing
SPACING = 20
#zooming
ZOOMSENSITIVITY = 2  # Adjust the zoom speed
MINZOOM = -12         # Minimum zoom level
MAXZOOM = 15          # Maximum zoom level
#colors
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (1, 153, 255)
HIGHLIGHT_TEXT_COLOR = (100, 249, 247)  # Highlight color
BLUETEXT = (1, 153, 255) # dark blue for labels
SELECTEDCOMP = (1, 153, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 153, 255)
BLACK = (0, 0, 0)
DARKBLUE = (0,31,56)
ORANGE = (255,175,0)
BROWN = (130,60,0)
YELLOW = (255,255,0)
GREEN = (0,200,30)
#general
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
LABEL_WIDTH, LABEL_HEIGHT = 150, 50
IMAGE_WIDTH, IMAGE_HEIGHT = 80, 80  # Height is kept the same for now
FONT_SIZE = 20
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (50, 50, 200)
BUTTON_HOVER_COLOR = (70, 70, 255)
TEXT_COLOR = (255, 255, 255)

DROPDOWN_DELAY = 800  # Delay before hiding the dropdown (in ms)

font = pygame.font.Font("C:/Users/marte/AppData/Local/Microsoft/Windows/Fonts/Poppins-Medium.ttf", 12)
font2 = pygame.font.Font("C:/Users/marte/AppData/Local/Microsoft/Windows/Fonts/Poppins-Medium.ttf", 14)
font3 = pygame.font.Font("C:/Users/marte/AppData/Local/Microsoft/Windows/Fonts/Poppins-Medium.ttf", 16)
font4 = pygame.font.Font("C:/Users/marte/AppData/Local/Microsoft/Windows/Fonts/Goldman-Regular.ttf", 24)
font5 = pygame.font.Font("C:/Users/marte/AppData/Local/Microsoft/Windows/Fonts/Poppins-Medium.ttf", 11)
