from main.global_constants import screen, font2, LIGHT_GRAY, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, BLUE
from pymongo import MongoClient
import pygame
from bson import ObjectId

client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
panel_open = False
input_active = False
input_text = ""
input_box = pygame.Rect(0, 0, 120, 30)
selected_class_id = None

# Add a cache for classes and a flag to refresh
cached_classes = []
classes_need_refresh = True

# Invite input state
invite_input_active = False
invite_input_text = ""

# Add repo input state
addrepo_input_active = False
addrepo_input_text = ""

def get_classes_for_user(user_id):
    """Return list of classes for a given user ObjectId."""
    return list(db.classes.find({"owner": ObjectId(user_id)}))

def get_class_members(class_id):
    """Return list of usernames for members in a class."""
    class_doc = db.classes.find_one({"_id": ObjectId(class_id)})
    if class_doc and "members" in class_doc and class_doc["members"]:
        # Assuming members is a list of user IDs, fetch usernames
        member_ids = class_doc["members"]
        users = db.users.find({"_id": {"$in": member_ids}})
        return [user.get("username", "unknown") for user in users]
    return []

def get_classes_user_is_member_of(user_id):
    """Return list of classes where user is a member."""
    return list(db.classes.find({"members": ObjectId(user_id)}))

def manage_classes_button(mouse_pos, left_mouse_button, user_id, event, username):
    global panel_open, input_active, input_text, input_box, selected_class_id
    global cached_classes, classes_need_refresh
    global invite_input_active, invite_input_text
    global addrepo_input_active, addrepo_input_text

    # Always refresh selected_class_doc if a class is selected
    selected_class_doc = None
    if selected_class_id:
        selected_class_doc = db.classes.find_one({"_id": ObjectId(selected_class_id)})

    manage_text = font2.render("manage classes", True, WHITE)
    managerect = manage_text.get_rect(topleft=(1100, 15))
    screen.blit(manage_text, managerect)

    if managerect.collidepoint(mouse_pos) and left_mouse_button:
        panel_open = True
        classes_need_refresh = True  # Refresh classes when panel is opened

    if panel_open:
        menu_image = pygame.image.load("./images/menus/classes.png")
        menu_rect = menu_image.get_rect(center=((SCREEN_WIDTH // 2) + 100, SCREEN_HEIGHT // 2))
        screen.blit(menu_image, menu_rect)

        Iteach_text = font2.render("classes I teach", True, WHITE)
        Iteach_x = menu_rect.left + 150
        Iteach_y = menu_rect.top + 100
        Iteachrect = Iteach_text.get_rect(center=(Iteach_x, Iteach_y))
        screen.blit(Iteach_text, Iteachrect)

        # --- Classes Table ---
        # Only fetch from DB if needed
        if classes_need_refresh and user_id:
            cached_classes = get_classes_for_user(user_id)
            classes_need_refresh = False
        classes = cached_classes if user_id else []
        class_rects = []
        table_x = Iteachrect.left
        table_y = Iteachrect.bottom + 40
        rect_width = 120
        rect_height = 30
        margin_bottom = 20

        for idx, class_doc in enumerate(classes):
            rect_y = table_y + idx * (rect_height + margin_bottom)
            rect_color = (230, 230, 230) if idx % 2 == 0 else (255, 255, 255)
            if selected_class_id == str(class_doc["_id"]):
                rect_color = BLUE
            rect = pygame.Rect(table_x, rect_y, rect_width, rect_height)
            class_rects.append((rect, class_doc))
            pygame.draw.rect(screen, rect_color, rect, border_radius=5)
            class_name_color = WHITE if selected_class_id == str(class_doc["_id"]) else (0, 0, 0)
            class_name_text = font2.render(class_doc["name"], True, class_name_color)
            screen.blit(class_name_text, class_name_text.get_rect(center=rect.center))

        # Handle class selection
        if left_mouse_button:
            for rect, class_doc in class_rects:
                if rect.collidepoint(mouse_pos):
                    selected_class_id = str(class_doc["_id"])

        my_classes_text = font2.render("my classes", True, WHITE)
        my_classes_x = menu_rect.left + 450
        my_classes_y = menu_rect.top + 100
        my_classes_rect = my_classes_text.get_rect(center=(my_classes_x, my_classes_y))
        screen.blit(my_classes_text, my_classes_rect)

        # --- Display classes user is a member of ---
        member_classes = get_classes_user_is_member_of(user_id) if user_id else []
        member_table_x = my_classes_rect.left
        member_table_y = my_classes_rect.bottom + 40
        member_rect_width = 120
        member_rect_height = 30
        member_margin_bottom = 20

        for idx, class_doc in enumerate(member_classes):
            rect_y = member_table_y + idx * (member_rect_height + member_margin_bottom)
            rect_color = (230, 230, 230) if idx % 2 == 0 else (255, 255, 255)
            rect = pygame.Rect(member_table_x, rect_y, member_rect_width, member_rect_height)
            pygame.draw.rect(screen, rect_color, rect, border_radius=5)
            class_name_text = font2.render(class_doc["name"], True, (0, 0, 0))
            screen.blit(class_name_text, class_name_text.get_rect(center=rect.center))

        # Show selected class name in repositories in {classname}
        selected_class_name = "..."  # default
        for class_doc in classes:
            if selected_class_id == str(class_doc["_id"]):
                selected_class_name = class_doc["name"]
                break
        repositories_in_text = font2.render(f"repositories in {selected_class_name}", True, WHITE)
        repositories_in_x = menu_rect.left + 750
        repositories_in_y = menu_rect.top + 100
        repositories_in_rect = repositories_in_text.get_rect(center=(repositories_in_x, repositories_in_y))
        screen.blit(repositories_in_text, repositories_in_rect)

        members_text = font2.render("members", True, WHITE)
        members_x = menu_rect.left + 1050
        members_y = menu_rect.top + 100
        members_rect = members_text.get_rect(center=(members_x, members_y))
        screen.blit(members_text, members_rect)

        # --- Display members under "members" ---
        members_list = []
        if selected_class_id:
            members_list = get_class_members(selected_class_id)
        members_display_y = members_rect.bottom + 10
        if selected_class_id:
            if members_list:
                for idx, member in enumerate(members_list):
                    member_text = font2.render(member, True, (0, 0, 0))
                    member_rect = member_text.get_rect(left=members_rect.left, top=members_display_y + idx * 30)
                    screen.blit(member_text, member_rect)
            else:
                none_text = font2.render("none", True, (100, 100, 100))
                none_rect = none_text.get_rect(left=members_rect.left, top=members_display_y)
                screen.blit(none_text, none_rect)

        cross_img = pygame.image.load("./images/icons/cross.png")
        cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
        cross_rect = cross_img.get_rect(topright=(menu_rect.right - 10, menu_rect.top + 10))
        screen.blit(cross_img, cross_rect)

        if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
            panel_open = False
            input_active = False

        create_text = font2.render("Create Class", True, WHITE)
        upload_text = font2.render("Upload File", True, WHITE)
        addrepo_text = font2.render("add repo", True, WHITE)
        invite_text = font2.render("Invite", True, WHITE)

        createclass_rect = pygame.Rect(0, 0, create_text.get_width() + 10, create_text.get_height() + 10)
        createclass_rect.center = (menu_rect.left + 180, menu_rect.bottom - 80)
        uploadfile_rect = pygame.Rect(0, 0, upload_text.get_width() + 10, upload_text.get_height() + 10)
        uploadfile_rect.center = (menu_rect.left + 800, menu_rect.bottom - 50)
        addrepo_rect = pygame.Rect(0, 0, addrepo_text.get_width() + 10, addrepo_text.get_height() + 10)
        addrepo_rect.center = (menu_rect.left + 800, menu_rect.bottom - 80)
        invite_rect = pygame.Rect(0, 0, invite_text.get_width() + 10, invite_text.get_height() + 10)
        invite_rect.center = (menu_rect.left + 1050, menu_rect.bottom - 80)

        pygame.draw.rect(screen, BLUE, createclass_rect, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, uploadfile_rect, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, invite_rect, border_radius=5)
        pygame.draw.rect(screen, LIGHT_GRAY, addrepo_rect, border_radius=5)

        screen.blit(create_text, (createclass_rect.x + 5, createclass_rect.y + 5))
        screen.blit(upload_text, (uploadfile_rect.x + 5, uploadfile_rect.y + 5))
        screen.blit(invite_text, (invite_rect.x + 5, invite_rect.y + 5))
        screen.blit(addrepo_text, (addrepo_rect.x + 5, addrepo_rect.y + 5))

        input_box.top = createclass_rect.top
        input_box.right = createclass_rect.left - 10

        if input_box.collidepoint(mouse_pos) and left_mouse_button:
            input_active = True
            input_text = ""

        if input_active and event:
            if event.key == pygame.K_RETURN:
                input_active = False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif len(input_text) < 30:
                input_text += event.unicode

        if createclass_rect.collidepoint(mouse_pos) and left_mouse_button:
            if input_text.strip():
                db.classes.insert_one({"name": input_text.strip(), "owner": ObjectId(user_id)})
                classes_need_refresh = True  # Mark to refresh after adding
            input_text = ""
            input_active = False

        pygame.draw.rect(screen, WHITE, input_box, border_radius=5)  # Fill white
        border_color = BLUE if input_active else WHITE
        pygame.draw.rect(screen, border_color, input_box, width=2, border_radius=5)

        input_surface = font2.render(input_text, True, (0, 0, 0))  # Use black for visible input
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

        # Invite button logic
        invite_enabled = selected_class_id is not None
        invite_btn_color = BLUE if invite_enabled else LIGHT_GRAY

        # Invite input field
        invite_input_box = pygame.Rect(0, 0, 120, 30)
        invite_input_box.top = invite_rect.top
        invite_input_box.right = invite_rect.left - 10

        # Draw invite input box
        pygame.draw.rect(screen, WHITE, invite_input_box, border_radius=5)
        invite_border_color = BLUE if invite_input_active else WHITE
        pygame.draw.rect(screen, invite_border_color, invite_input_box, width=2, border_radius=5)
        invite_input_surface = font2.render(invite_input_text, True, (0, 0, 0))
        screen.blit(invite_input_surface, (invite_input_box.x + 5, invite_input_box.y + 5))

        # Draw invite button (overwrite previous)
        pygame.draw.rect(screen, invite_btn_color, invite_rect, border_radius=5)
        screen.blit(invite_text, (invite_rect.x + 5, invite_rect.y + 5))

        # Handle invite input activation
        if invite_input_box.collidepoint(mouse_pos) and left_mouse_button:
            invite_input_active = True
            invite_input_text = ""
        elif not invite_input_box.collidepoint(mouse_pos) and left_mouse_button:
            invite_input_active = False

        # Handle invite input typing
        if invite_input_active and event:
            if event.key == pygame.K_RETURN:
                invite_input_active = False
            elif event.key == pygame.K_BACKSPACE:
                invite_input_text = invite_input_text[:-1]
            elif len(invite_input_text) < 30:
                invite_input_text += event.unicode

        # Handle invite button click
        if invite_enabled and invite_rect.collidepoint(mouse_pos) and left_mouse_button:
            if invite_input_text.strip():
                db.invites.insert_one({
                    "from": username,
                    "to": invite_input_text.strip(),
                    "class_id": ObjectId(selected_class_id)
                })
                invite_input_text = ""
                invite_input_active = False

        # Determine if selected class is taught by user
        selected_class_is_taught_by_user = False
        if selected_class_id:
            for class_doc in classes:
                if selected_class_id == str(class_doc["_id"]):
                    if str(class_doc.get("owner")) == str(user_id):
                        selected_class_is_taught_by_user = True
                    break

        # Add repo input box (to the left of addrepo button)
        addrepo_input_box = pygame.Rect(0, 0, 120, 30)
        addrepo_input_box.top = addrepo_rect.top
        addrepo_input_box.right = addrepo_rect.left - 10

        # Draw addrepo input box
        pygame.draw.rect(screen, WHITE, addrepo_input_box, border_radius=5)
        addrepo_border_color = BLUE if addrepo_input_active else WHITE
        pygame.draw.rect(screen, addrepo_border_color, addrepo_input_box, width=2, border_radius=5)
        addrepo_input_surface = font2.render(addrepo_input_text, True, (0, 0, 0))
        screen.blit(addrepo_input_surface, (addrepo_input_box.x + 5, addrepo_input_box.y + 5))

        # Draw addrepo button
        addrepo_btn_color = BLUE if selected_class_is_taught_by_user else LIGHT_GRAY
        pygame.draw.rect(screen, addrepo_btn_color, addrepo_rect, border_radius=5)
        screen.blit(addrepo_text, (addrepo_rect.x + 5, addrepo_rect.y + 5))

        # Handle addrepo input activation
        if addrepo_input_box.collidepoint(mouse_pos) and left_mouse_button:
            addrepo_input_active = True
            addrepo_input_text = ""
        elif not addrepo_input_box.collidepoint(mouse_pos) and left_mouse_button:
            addrepo_input_active = False

        # Handle addrepo input typing
        if addrepo_input_active and event:
            if event.key == pygame.K_RETURN:
                addrepo_input_active = False
            elif event.key == pygame.K_BACKSPACE:
                addrepo_input_text = addrepo_input_text[:-1]
            elif len(addrepo_input_text) < 30:
                addrepo_input_text += event.unicode

        # Handle addrepo button click
        if selected_class_is_taught_by_user and addrepo_rect.collidepoint(mouse_pos) and left_mouse_button:
            if addrepo_input_text.strip():
                db.classes.update_one(
                    {"_id": ObjectId(selected_class_id)},
                    {"$addToSet": {"repositories": addrepo_input_text.strip()}}
                )
                addrepo_input_text = ""
                addrepo_input_active = False
                # Refresh selected_class_doc so new repo appears immediately
                selected_class_doc = db.classes.find_one({"_id": ObjectId(selected_class_id)})

        # --- Display repositories for selected class ---
        repo_list = []
        if selected_class_doc and "repositories" in selected_class_doc:
            repo_list = selected_class_doc["repositories"]
        repo_table_x = repositories_in_rect.left
        repo_table_y = repositories_in_rect.bottom + 10
        repo_rect_width = 120
        repo_rect_height = 30
        repo_margin_bottom = 10

        for idx, repo_name in enumerate(repo_list):
            rect_y = repo_table_y + idx * (repo_rect_height + repo_margin_bottom)
            rect_color = (230, 230, 230) if idx % 2 == 0 else (255, 255, 255)
            repo_rect = pygame.Rect(repo_table_x, rect_y, repo_rect_width, repo_rect_height)
            pygame.draw.rect(screen, rect_color, repo_rect, border_radius=5)
            repo_name_text = font2.render(repo_name, True, (0, 0, 0))
            screen.blit(repo_name_text, repo_name_text.get_rect(center=repo_rect.center))

        # --- Rest of the code remains unchanged ---
