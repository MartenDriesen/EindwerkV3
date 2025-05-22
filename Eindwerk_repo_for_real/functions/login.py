import pygame
from pymongo import MongoClient
from main.global_constants import font, screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, LIGHT_BLUE, BLACK, BLUE, font2
import os

# Load environment variables


# MongoDB connection
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
users_collection = db["users"]

# UI Elements
login_menu_image = pygame.image.load("./images/menus/properties.png")
login_menu_image = pygame.transform.smoothscale(login_menu_image, (350, 245))
login_menu_rect = login_menu_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# State variables
input_active = {"name": False, "password": False}
user_input = {"name": "", "password": ""}
status_message = ""
ok = False
logged_user = None

def draw_login_register_menu(event, mouse_pos, mouse_click):
    global input_active, user_input, status_message, ok, logged_user

    # Draw background menu
    screen.blit(login_menu_image, login_menu_rect)

    # Layout
    menu_center_x = login_menu_rect.centerx
    top = login_menu_rect.top + 20
    spacing = 30
    field_width = 250
    field_height = 30

    # Input rects
    name_rect = pygame.Rect(0, 0, field_width, field_height)
    name_rect.centerx = menu_center_x
    name_rect.top = top + 50

    pass_rect = pygame.Rect(0, 0, field_width, field_height)
    pass_rect.centerx = menu_center_x
    pass_rect.top = name_rect.bottom + spacing

    # Labels
    name_label = font.render("Name", True, WHITE)
    password_label = font.render("Password", True, WHITE)
    screen.blit(name_label, name_label.get_rect(midleft=(name_rect.left, name_rect.top - 18)))
    screen.blit(password_label, password_label.get_rect(midleft=(pass_rect.left, pass_rect.top - 18)))

    # Input fields
    for key, rect in [("name", name_rect), ("password", pass_rect)]:
        if input_active[key]:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLUE, rect, 2)
        else:
            pygame.draw.rect(screen, WHITE, rect)

    name_text = font.render(user_input["name"], True, BLACK)
    pass_text = font.render("*" * len(user_input["password"]), True, BLACK)
    screen.blit(name_text, (name_rect.x + 5, name_rect.y + 5))
    screen.blit(pass_text, (pass_rect.x + 5, pass_rect.y + 5))

    if mouse_click:

        if name_rect.collidepoint(mouse_pos):
            input_active["name"] = True
            input_active["password"] = False
        elif pass_rect.collidepoint(mouse_pos):
            input_active["password"] = True
            input_active["name"] = False
        else:
            input_active["name"] = False
            input_active["password"] = False


    # Typing input
    if event:
        active_key = "name" if input_active["name"] else "password" if input_active["password"] else None
        if active_key:
            if event.key == pygame.K_BACKSPACE:
                user_input[active_key] = user_input[active_key][:-1]
            elif event.key == pygame.K_RETURN:
                input_active["name"] = False
                input_active["password"] = False
            elif len(user_input[active_key]) < 20 and event.unicode.isprintable():
                user_input[active_key] += event.unicode

    # Buttons
    button_width = 120
    button_height = 30
    button_spacing = 10

    login_rect = pygame.Rect(0, 0, button_width, button_height)
    register_rect = pygame.Rect(0, 0, button_width, button_height)

    total_width = 2 * button_width + button_spacing
    login_rect.left = menu_center_x - total_width // 2
    register_rect.left = login_rect.right + button_spacing

    login_rect.top = pass_rect.bottom + 50
    register_rect.top = login_rect.top

    # Status message above buttons
    if status_message:
        status_render = font.render(status_message, True, WHITE)
        status_rect = status_render.get_rect(center=(menu_center_x, login_rect.top - 30))
        screen.blit(status_render, status_rect)

    # Draw buttons
    pygame.draw.rect(screen, LIGHT_BLUE, login_rect, border_radius=6)
    pygame.draw.rect(screen, LIGHT_BLUE, register_rect, border_radius=6)

    login_text = font.render("Login", True, WHITE)
    register_text = font.render("Register", True, WHITE)
    screen.blit(login_text, login_text.get_rect(center=login_rect.center))
    screen.blit(register_text, register_text.get_rect(center=register_rect.center))

    # Handle button clicks
    if mouse_click and mouse_pos:
        if register_rect.collidepoint(mouse_pos):
            status_message = handle_register()
        elif login_rect.collidepoint(mouse_pos):
            status_message = handle_login()

    # ✅ Return username and user_id if successful, else None
    if ok:
        user_input["name"] = ""
        user_input["password"] = ""
        status_message = ""
        print(str(logged_user["_id"]))
        return logged_user["username"], str(logged_user["_id"])
    return None, None

def handle_register():
    global ok, logged_user
    if not user_input["name"] or not user_input["password"]:
        return "❌ fill in all fields"
    try:
        existing = users_collection.find_one({"username": user_input["name"]})
        if existing:
            return "❌ user already exists"
        result = users_collection.insert_one({
            "username": user_input["name"],
            "password": user_input["password"]
        })
        # Fetch the inserted user with _id
        logged_user = users_collection.find_one({"_id": result.inserted_id})
    except Exception as e:
        return f"❌ Databasefout: {str(e)}"
    ok = True
    return "✅ registered!"


def handle_login():
    global logged_user, ok
    try:
        user = users_collection.find_one({"username": user_input["name"]})
        if not user:
            return "user not found"
        elif user["password"] != user_input["password"]:
            return "wrong password"
    except Exception as e:
        print(e)
        return f"❌ Databasefout: {str(e)}"
        return "Gebruiker niet gevonden"
    if user["password"] != user_input["password"]:
        return "wrong password"
    logged_user = user
    ok = True
    return "✅ logged in!"

def logout(mouse_pos, mouse_click):
    global logged_user, ok
    logout_text = font2.render("Logout", True, WHITE)

    logout_rect = logout_text.get_rect(topleft=(1300, 12))
    screen.blit(logout_text, logout_rect)
    if mouse_click and logout_rect.collidepoint(mouse_pos):
        logged_user = None
        ok = False
        return True
    return False
  
def show_user(username):
    if username:
        user_text = font2.render(f"user: {username}", True, WHITE)
        userrect = user_text.get_rect(topleft=(1400, 12))
        screen.blit(user_text, userrect)