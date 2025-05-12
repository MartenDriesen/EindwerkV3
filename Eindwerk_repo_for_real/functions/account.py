import pygame
from pymongo import MongoClient
from main.global_constants import font, screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, LIGHT_BLUE

# MongoDB connectie
from dotenv import load_dotenv
import os
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["powerlink"]
users_collection = db["users"]

# Achtergrond en posities
login_menu_image = pygame.image.load("./images/menus/properties.png")
login_menu_image = pygame.transform.smoothscale(login_menu_image, (350, 245))
login_menu_rect = login_menu_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

button_padding = 8
input_active = {"name": False, "password": False}
user_input = {"name": "", "password": ""}
status_message = ""
ok = None
logged_user = None

def draw_login_register_menu(event=None, mouse_pos=None, mouse_click=False):
    global input_active, user_input, status_message, logged_user

    screen.blit(login_menu_image, login_menu_rect)

    # Layout constants
    start_x = login_menu_rect.left + 20
    input_x = start_x + 100
    input_width = 180
    input_height = 30
    line_spacing = 60

    # First row (Name)
    name_label = font.render("Name", True, WHITE)
    screen.blit(name_label, (start_x, login_menu_rect.top + 20))

    name_rect = pygame.Rect(input_x, login_menu_rect.top + 15, input_width, input_height)
    pygame.draw.rect(screen, WHITE, name_rect, 0, border_radius=4)
    name_text = font.render(user_input["name"], True, (0, 0, 0))
    screen.blit(name_text, (name_rect.x + 5, name_rect.y + 5))

    # Second row (Password)
    password_label = font.render("Password", True, WHITE)
    screen.blit(password_label, (start_x, login_menu_rect.top + 20 + line_spacing))

    pass_rect = pygame.Rect(input_x, login_menu_rect.top + 15 + line_spacing, input_width, input_height)
    pygame.draw.rect(screen, WHITE, pass_rect, 0, border_radius=4)
    pass_display = "*" * len(user_input["password"])
    pass_text = font.render(pass_display, True, (0, 0, 0))
    screen.blit(pass_text, (pass_rect.x + 5, pass_rect.y + 5))

    # Detect active input
    if mouse_click:
        input_active["name"] = name_rect.collidepoint(mouse_pos)
        input_active["password"] = pass_rect.collidepoint(mouse_pos)

    # Handle typing
    if event and event.type == pygame.KEYDOWN:
        active_key = "name" if input_active["name"] else "password" if input_active["password"] else None
        if active_key:
            if event.key == pygame.K_BACKSPACE:
                user_input[active_key] = user_input[active_key][:-1]
            elif event.key == pygame.K_RETURN:
                input_active["name"] = False
                input_active["password"] = False
            elif len(event.unicode) > 0 and len(user_input[active_key]) < 25:
                user_input[active_key] += event.unicode

    # Buttons
    login_rect = pygame.Rect(login_menu_rect.centerx - 60, login_menu_rect.bottom - 70, 120, 25)
    register_rect = pygame.Rect(login_menu_rect.centerx - 60, login_menu_rect.bottom - 40, 120, 25)

    pygame.draw.rect(screen, LIGHT_BLUE, login_rect, 0, border_radius=6)
    pygame.draw.rect(screen, LIGHT_BLUE, register_rect, 0, border_radius=6)

    login_text = font.render("Login", True, WHITE)
    register_text = font.render("Register", True, WHITE)

    screen.blit(login_text, login_text.get_rect(center=login_rect.center))
    screen.blit(register_text, register_text.get_rect(center=register_rect.center))

    # Handle click
    if mouse_click:
        if register_rect.collidepoint(mouse_pos):
            status_message = handle_register()
        elif login_rect.collidepoint(mouse_pos):
            status_message = handle_login()

    # Status message
    if status_message:
        status_render = font.render(status_message, True, WHITE)
        screen.blit(status_render, (login_menu_rect.left + 20, login_menu_rect.bottom - 100))

    return (logged_user, True) if logged_user else (None, False)



def handle_register():
    global ok, logged_user
    existing = users_collection.find_one({"name": user_input["name"]})
    if existing:
        return "❌ Gebruiker bestaat al"
    else:
        users_collection.insert_one({
            "name": user_input["name"],
            "password": user_input["password"]
        })
        logged_user = user_input
    return "✅ Geregistreerd!"

def handle_login():
    global ok, logged_user
    user = users_collection.find_one({"name": user_input["name"]})
    if not user:
        return "❌ Gebruiker niet gevonden"
    elif user["password"] != user_input["password"]:
        return "❌ Fout wachtwoord"
    else:
        logged_user = user
    return "✅ Ingelogd!"
