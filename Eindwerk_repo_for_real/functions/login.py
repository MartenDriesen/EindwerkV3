import pygame
from pymongo import MongoClient
from main.global_constants import font, screen, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, LIGHT_BLUE, BLACK, BLUE, font2, GREEN
import os

# Load environment variables


# MongoDB connection
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
users_collection = db["users"]

# UI Elements
login_menu_image = pygame.image.load("./images/menus/properties.png")
login_menu_image = pygame.transform.smoothscale(login_menu_image, (350, 270))
login_menu_rect = login_menu_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# New: Load back/cross image for back button
back_img = pygame.image.load("./images/icons/back.png")
back_img = pygame.transform.smoothscale(back_img, (10, 15))

# State variables
input_active = {"name": False, "password": False}
user_input = {"name": "", "password": ""}
status_message = ""
ok = False
logged_user = None

# New: State for menu navigation and register role
login_menu_state = "choose"  # can be "choose", "login", "register"
is_teacher = False

def draw_checkbox(x, y, checked, color=BLUE):
    size = 20
    pygame.draw.rect(screen, WHITE, (x, y, size, size))
    if checked:
        padding = 5
        pygame.draw.rect(screen, color, (x + padding, y + padding, size - 2*padding, size - 2*padding))
    return pygame.Rect(x, y, size, size)

def draw_login_register_menu(event, mouse_pos, mouse_click):
    global input_active, user_input, status_message, ok, logged_user
    global login_menu_state, is_teacher

    # Draw background menu
    screen.blit(login_menu_image, login_menu_rect)

    menu_center_x = login_menu_rect.centerx
    top = login_menu_rect.top + 20
    spacing = 30
    field_width = 250
    field_height = 30

    # Initial choose menu
    if login_menu_state == "choose":
        # Use original button size
        button_width = 120
        button_height = 30
        button_spacing = 30
        login_rect = pygame.Rect(0, 0, button_width, button_height)
        register_rect = pygame.Rect(0, 0, button_width, button_height)
        login_rect.centerx = menu_center_x
        register_rect.centerx = menu_center_x
        login_rect.centery = login_menu_rect.centery - button_height
        register_rect.centery = login_menu_rect.centery + button_height

        pygame.draw.rect(screen, LIGHT_BLUE, login_rect, border_radius=6)
        pygame.draw.rect(screen, LIGHT_BLUE, register_rect, border_radius=6)
        login_text = font2.render("login", True, WHITE)
        register_text = font2.render("Register", True, WHITE)
        screen.blit(login_text, login_text.get_rect(center=login_rect.center))
        screen.blit(register_text, register_text.get_rect(center=register_rect.center))

        if mouse_click and mouse_pos:
            if login_rect.collidepoint(mouse_pos):
                login_menu_state = "login"
                status_message = ""
            elif register_rect.collidepoint(mouse_pos):
                login_menu_state = "register"
                status_message = ""
        return None, None

    # Draw back button (top left)
    back_rect = back_img.get_rect(topleft=(login_menu_rect.left + 25, login_menu_rect.top + 40))
    screen.blit(back_img, back_rect)
    if mouse_click and back_rect.collidepoint(mouse_pos):
        login_menu_state = "choose"
        input_active = {"name": False, "password": False}
        user_input = {"name": "", "password": ""}
        status_message = ""
        is_teacher = False
        return None, None

    # Layout for login/register
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
    enter_pressed = False
    if event:
        active_key = "name" if input_active["name"] else "password" if input_active["password"] else None
        if active_key:
            if event.key == pygame.K_BACKSPACE:
                user_input[active_key] = user_input[active_key][:-1]
            elif event.key == pygame.K_RETURN:
                input_active["name"] = False
                input_active["password"] = False
                enter_pressed = True
            elif len(user_input[active_key]) < 20 and event.unicode.isprintable():
                user_input[active_key] += event.unicode
        elif event.key == pygame.K_RETURN:
            enter_pressed = True

    # Register: teacher/student checkboxes under each other, left align with input fields, label right of box
    teacher_rect = student_rect = None
    if login_menu_state == "register":
        checkbox_x = name_rect.left  # left align with input box
        teacher_y = pass_rect.bottom + 30
        student_y = teacher_y + 30
        # Teacher checkbox is green, student is blue
        teacher_rect = draw_checkbox(checkbox_x, teacher_y, is_teacher, color=GREEN)
        student_rect = draw_checkbox(checkbox_x, student_y, not is_teacher, color=BLUE)
        label_teacher = font.render("I'm teacher", True, WHITE)
        label_student = font.render("I'm student", True, WHITE)
        screen.blit(label_teacher, (teacher_rect.right + 10, teacher_rect.y - 2))
        screen.blit(label_student, (student_rect.right + 10, student_rect.y - 2))

        # Handle checkbox clicks
        if mouse_click and mouse_pos:
            if teacher_rect.collidepoint(mouse_pos):
                is_teacher = True
            elif student_rect.collidepoint(mouse_pos):
                is_teacher = False

    # Buttons
    button_width = 120
    button_height = 30

    if login_menu_state == "register":
        register_rect = pygame.Rect(0, 0, button_width, button_height)
        # Align right with input box, 10px higher than before
        register_rect.right = name_rect.right
        register_rect.top = pass_rect.bottom + 40  # was +50, now +40
        # Status message above button
        if status_message:
            status_render = font.render(status_message, True, WHITE)
            status_rect = status_render.get_rect(center=(menu_center_x, register_rect.top - 30))
            screen.blit(status_render, status_rect)
        pygame.draw.rect(screen, LIGHT_BLUE, register_rect, border_radius=6)
        register_text = font2.render("Register", True, WHITE)
        screen.blit(register_text, register_text.get_rect(center=register_rect.center))
        if mouse_click and mouse_pos and register_rect.collidepoint(mouse_pos):
            status_message = handle_register()
        # Allow pressing Enter to register
        elif enter_pressed:
            status_message = handle_register()
    else:
        login_rect = pygame.Rect(0, 0, button_width, button_height)
        login_rect.centerx = menu_center_x
        login_rect.top = pass_rect.bottom + 40  # was +50, now +40
        # Status message above button
        if status_message:
            status_render = font.render(status_message, True, WHITE)
            status_rect = status_render.get_rect(center=(menu_center_x, login_rect.top - 30))
            screen.blit(status_render, status_rect)
        pygame.draw.rect(screen, LIGHT_BLUE, login_rect, border_radius=6)
        login_text = font2.render("Login", True, WHITE)
        screen.blit(login_text, login_text.get_rect(center=login_rect.center))
        if mouse_click and mouse_pos and login_rect.collidepoint(mouse_pos):
            status_message = handle_login()
        # Allow pressing Enter to login
        elif enter_pressed:
            status_message = handle_login()

    # ✅ Return username and user_id and is_teacher if successful, else None
    if ok:
        user_input["name"] = ""
        user_input["password"] = ""
        status_message = ""
        login_menu_state = "choose"
        # Set is_teacher from logged_user if available
        if logged_user and "logged_as_teacher" in logged_user:
            is_teacher = logged_user["logged_as_teacher"]
        else:
            is_teacher = False
        print(str(logged_user["_id"]))
        return logged_user["username"], str(logged_user["_id"]), is_teacher
    return None, None, is_teacher

def handle_register():
    global ok, logged_user, is_teacher
    if not user_input["name"] or not user_input["password"]:
        return "❌ fill in all fields"
    # Only one checkbox, so always a value
    try:
        existing = users_collection.find_one({"username": user_input["name"]})
        if existing:
            return "❌ user already exists"
        result = users_collection.insert_one({
            "username": user_input["name"],
            "password": user_input["password"],
            "logged_as_teacher": is_teacher
        })
        # Fetch the inserted user with _id
        logged_user = users_collection.find_one({"_id": result.inserted_id})
    except Exception as e:
        return f"❌ Databasefout: {str(e)}"
    ok = True
    return "✅ registered!"


def handle_login():
    global logged_user, ok, is_teacher
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
    # Set is_teacher from db
    is_teacher = user.get("logged_as_teacher", False)
    ok = True
    return "✅ logged in!"

def logout(mouse_pos, mouse_click):
    global logged_user, ok
    logout_text = font2.render("Logout", True, WHITE)

    logout_rect = logout_text.get_rect(topleft=(1250, 12))
    screen.blit(logout_text, logout_rect)
    if mouse_click and logout_rect.collidepoint(mouse_pos):
        logged_user = None
        ok = False
        return True
    return False
  
def show_user(username, is_teacher):
    role = "Teacher" if is_teacher else "Student"
    # Use white color for teacher (with green underline), white for student
    if username:
        if role == "Teacher":
            role_text = font2.render(f"{role}:", True, WHITE)
            user_text = font2.render(f" {username}", True, WHITE)
            # Position role and username next to each other
            role_rect = role_text.get_rect(topleft=(1350, 12))
            user_rect = user_text.get_rect(topleft=(role_rect.right, 12))
            screen.blit(role_text, role_rect)
            # Draw green underline for "Teacher:"
            underline_y = role_rect.bottom + 2
            pygame.draw.line(screen, GREEN, (role_rect.left, underline_y), (role_rect.right, underline_y), 3)
            screen.blit(user_text, user_rect)
        else:
            role_text = font2.render(f"{role}:", True, WHITE)
            user_text = font2.render(f" {username}", True, WHITE)
            role_rect = role_text.get_rect(topleft=(1350, 12))
            user_rect = user_text.get_rect(topleft=(role_rect.right, 12))
            screen.blit(role_text, role_rect)
            screen.blit(user_text, user_rect)