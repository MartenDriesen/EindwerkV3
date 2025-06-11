from main.global_constants import screen, font2, LIGHT_GRAY, WHITE, SCREEN_HEIGHT, SCREEN_WIDTH, BLUE, GREEN, font7
from pymongo import MongoClient
import pygame
from bson import ObjectId
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random
import string

classes= []
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
panel_open = False
input_active = False
input_text = ""
input_box = pygame.Rect(0, 0, 120, 30)
selected_class_id = None
selectedrepo = None
selected_file = None
files= None
member_class_answer = None  # Track if the user answered the leave confirmation
file_delete_answer = None  # Track if the user answered the delete confirmation
repo_delete_answer = None  # Track if the user answered the delete confirmation
remove_answer = None
answer = None  # Track if the user answered the delete confirmation
selected_file = None  # Track selected file for upload
# Add a cache for classes and a flag to refresh
cached_classes = []
classes_need_refresh = True
file_doc = None  # Track the file document for upload
# join input state
join_input_active = False
join_input_text = ""
selected_class_name = "(select a class)"
open_enabled = False# Track selected class name for displaying tasks

# Add repo input state
addrepo_input_active = False
addrepo_input_text = ""

selectedrepo = None  # Add this global variable to track selected repo

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

def generate_class_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def manage_classes_button(mouse_pos, left_mouse_button, user_id, event, username, is_teacher):
    global panel_open, input_active, input_text, input_box, selected_class_id, open_enabled
    global cached_classes, classes_need_refresh, remove_answer, files, selected_class_name
    global join_input_active, join_input_text, file_delete_answer, selected_file
    global addrepo_input_active, addrepo_input_text, repo_delete_answer, selectedrepo
    global selectedrepo, selected_file, file_doc, answer, member_class_answer, classes  # Add this
    comps, conns = None, None
    # Always refresh selected_class_doc if a class is selected
    selected_class_doc = None
    selected_class_role = None  # "teach" or "member"
    if selected_class_id:
        selected_class_doc = db.classes.find_one({"_id": ObjectId(selected_class_id)})
        if selected_class_doc:
            if str(selected_class_doc.get("owner")) == str(user_id):
                selected_class_role = "teach"
            elif ObjectId(user_id) in selected_class_doc.get("members", []):
                selected_class_role = "member"

    manage_text = font2.render("classes", True, WHITE)
    managerect = manage_text.get_rect(topleft=(1150, 12))
    screen.blit(manage_text, managerect)

    if managerect.collidepoint(mouse_pos) and left_mouse_button:
        panel_open = True
        classes_need_refresh = True  # Refresh classes when panel is opened

    if panel_open:

        if is_teacher:
            menu_image = pygame.image.load("./images/menus/classesgreen.png")
        else:
            menu_image = pygame.image.load("./images/menus/classes.png")
        menu_rect = menu_image.get_rect(center=((SCREEN_WIDTH // 2) + 100, SCREEN_HEIGHT // 2))
        screen.blit(menu_image, menu_rect)
        
        if is_teacher:
            Iteach_text = font7.render("classes I teach", True, WHITE)
            Iteach_x = menu_rect.left + 150
            Iteach_y = menu_rect.top + 100
            Iteachrect = Iteach_text.get_rect(center=(Iteach_x, Iteach_y))
            screen.blit(Iteach_text, Iteachrect)
            create_text = font2.render("Create Class", True, WHITE)
            createclass_rect = pygame.Rect(0, 0, create_text.get_width() + 10, create_text.get_height() + 10)
            createclass_rect.center = (menu_rect.left + 210, menu_rect.bottom - 80)
            pygame.draw.rect(screen, GREEN, createclass_rect, border_radius=5)
            screen.blit(create_text, (createclass_rect.x + 5, createclass_rect.y + 5))
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
                    class_code = generate_class_code()
                    db.classes.insert_one({
                        "name": input_text.strip(),
                        "owner": ObjectId(user_id),
                        "code": class_code
                    })
                    classes_need_refresh = True  # Mark to refresh after adding
                input_text = ""
                input_active = False

            pygame.draw.rect(screen, WHITE, input_box)  # Fill white
            border_color = BLUE if input_active else WHITE
            pygame.draw.rect(screen, border_color, input_box, width=2)

            input_surface = font2.render(input_text, True, (0, 0, 0))  # Use black for visible input
            screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            # --- Classes Table (taught by user) ---
            if classes_need_refresh and user_id:
                cached_classes = get_classes_for_user(user_id)
                classes_need_refresh = False
            classes = cached_classes if user_id else []
            class_rects = []
            table_x = Iteachrect.left - 40
            table_y = Iteachrect.bottom + 40
            rect_width = 120
            rect_height = 30
            margin_bottom = 20

            for idx, class_doc in enumerate(classes):
                rect_y = table_y + idx * (rect_height + margin_bottom)
                rect_color = (255, 255, 255)
                if selected_class_id == str(class_doc["_id"]):
                    rect_color = BLUE
                rect = pygame.Rect(table_x, rect_y, rect_width, rect_height)
                class_rects.append((rect, class_doc))
                pygame.draw.rect(screen, rect_color, rect)  # Draw the rectangle so it's visible
                class_name_color = WHITE if selected_class_id == str(class_doc["_id"]) else (0, 0, 0)
                class_name_text = font2.render(class_doc["name"], True, class_name_color)
                screen.blit(class_name_text, class_name_text.get_rect(center=rect.center))

                class_code = class_doc.get("code", "")
                code_text = font2.render(f"({class_code})", True, WHITE)
                code_rect = code_text.get_rect(midleft=(rect.right + 10, rect.centery))
                screen.blit(code_text, code_rect)                # Draw a cross icon to the right of the class rect
                cross_img = pygame.image.load("./images/icons/cross.png")
                cross_img = pygame.transform.smoothscale(cross_img, (8, 8))
                cross_x, cross_y  = rect.topleft

                cross_rect = cross_img.get_rect(midright=(cross_x, cross_y))
                screen.blit(cross_img, cross_rect)

                # Handle cross click for delete
                if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
                    root = tk.Tk()
                    root.withdraw()
                    answer = messagebox.askyesno(
                        "Delete Class",
                        f"Are you sure you want to delete class '{class_doc['name']}'?"
                    )
                    root.destroy()
                if answer:
                    db.classes.delete_one({"_id": class_doc["_id"]})
                    classes_need_refresh = True
                    answer = None  # Reset answer after deletion
                    # If deleted class was selected, reset selection
                    if selected_class_id == str(class_doc["_id"]):
                        selected_class_id = None
                        selectedrepo = None
                        selected_file = False
                        file_doc = None

            # Handle class selection
            if left_mouse_button:
                for rect, class_doc in class_rects:
                    if rect.collidepoint(mouse_pos):
                        selected_class_id = str(class_doc["_id"])
                        file_doc = None  # Reset file_doc when class is selected
                        selectedrepo = None  # Reset selected repo when class is selected
                        selected_file = False

        my_classes_text = font7.render("my classes", True, WHITE)
        my_classes_x = menu_rect.left + 450
        my_classes_y = menu_rect.top + 100
        my_classes_rect = my_classes_text.get_rect(center=(my_classes_x, my_classes_y))
        screen.blit(my_classes_text, my_classes_rect)

        # --- Display classes user is a member of ---
        member_classes = get_classes_user_is_member_of(user_id) if user_id else []
        # Center the member table under "my classes" text
        member_table_x = menu_rect.left + 450
        member_table_y = my_classes_rect.bottom + 40
        member_rect_width = 120
        member_rect_height = 30
        member_margin_bottom = 20

        # Track rects for member classes for selection
        member_class_rects = []

        for idx, class_doc in enumerate(member_classes):
            rect_y = member_table_y + idx * (member_rect_height + member_margin_bottom)
            rect_color = (230, 230, 230) if idx % 2 == 0 else (255, 255, 255)

            if selected_class_id == str(class_doc["_id"]):
                rect_color = BLUE
              

            # Create rect with dummy x (we'll override centerx)
            rect = pygame.Rect(0, rect_y, member_rect_width, member_rect_height)
            rect.centerx = member_table_x  # center on this x

            member_class_rects.append((rect, class_doc))
            pygame.draw.rect(screen, rect_color, rect)

            class_name_color = WHITE if selected_class_id == str(class_doc["_id"]) else (0, 0, 0)
            class_name_text = font2.render(class_doc["name"], True, class_name_color)
            screen.blit(class_name_text, class_name_text.get_rect(center=rect.center))

            # Draw out icon 10px to the left of the member class rect
            out_img = pygame.image.load("./images/icons/out.png")
            out_img = pygame.transform.smoothscale(out_img, (20, 20))
            out_x = rect.left - 30
            out_y = rect.centery - 10
            out_rect = out_img.get_rect(topleft=(out_x, out_y))
            screen.blit(out_img, out_rect)

            # Handle out icon click for leaving class
            if out_rect.collidepoint(mouse_pos) and left_mouse_button:
                root = tk.Tk()
                root.withdraw()
                member_class_answer = messagebox.askyesno(
                    "Leave Class",
                    f"Do you want to leave '{class_doc['name']}'?"
                )
                root.destroy()
                if member_class_answer:
                    # Remove user from class members
                    db.classes.update_one(
                    {"_id": class_doc["_id"]},
                    {"$pull": {"members": ObjectId(user_id)}}
                    )
                    # Remove class from user classes
                    db.users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$pull": {"classes": class_doc["_id"]}}
                    )
                    classes_need_refresh = True
                    member_class_answer = None  # Reset answer after leaving
                    # If left class was selected, reset selection
                    if selected_class_id == str(class_doc["_id"]):
                        selected_class_id = None
                        selectedrepo = None
                        selected_file = False
                        file_doc = None


        # Handle member class selection
        if left_mouse_button:
            for rect, class_doc in member_class_rects:
                if rect.collidepoint(mouse_pos):
                    selected_class_id = str(class_doc["_id"])
                    file_doc = None  # Reset file_doc when class is selected
                    selectedrepo = None  # Reset selected repo when class is selected
                    selected_file = False
                    selected_class_name = class_doc["name"]  # Store selected class name
        # Show selected class name in repositories in {classname}
        
        for class_doc in classes:
            if selected_class_id == str(class_doc["_id"]):
                selected_class_name = class_doc["name"]
                break
        repositories_in_text = font7.render(f"uploadzones in {selected_class_name}", True, WHITE)
        repositories_in_x = menu_rect.left + 750
        repositories_in_y = menu_rect.top + 100
        repositories_in_rect = repositories_in_text.get_rect(center=(repositories_in_x, repositories_in_y))
        screen.blit(repositories_in_text, repositories_in_rect)

        members_text = font7.render("members", True, WHITE)
        members_x = menu_rect.left + 1050
        members_y = menu_rect.top + 100
        members_rect = members_text.get_rect(center=(members_x, members_y))
        screen.blit(members_text, members_rect)

        # --- Display members under "members" ---
        members_list = []
        if selected_class_id:
            members_list = get_class_members(selected_class_id)
        members_display_y = members_rect.bottom + 40
        if selected_class_id:
            if members_list:
                for idx, member in enumerate(members_list):
                    member_text = font2.render(member, True, WHITE)
                    member_rect = member_text.get_rect(left=members_rect.left, top=members_display_y + idx * 30)
                    screen.blit(member_text, member_rect)

                    # Draw out.png 10px left of member_rect
                    if selected_class_role == "teach":
                        out_img = pygame.image.load("./images/icons/out.png")
                        out_img = pygame.transform.smoothscale(out_img, (20, 20))
                        out_x = member_rect.left - 30  # 10px left of member_rect
                        out_y = member_rect.top
                        out_rect = out_img.get_rect(topleft=(out_x, out_y))
                        screen.blit(out_img, out_rect)

                        # Only allow teacher to remove members (not themselves)
                        if (
                            selected_class_role == "teach"
                            and out_rect.collidepoint(mouse_pos)
                            and left_mouse_button
                            and member != username
                        ):
                            root = tk.Tk()
                            root.withdraw()
                            remove_answer = messagebox.askyesno(
                                "Remove Member",
                                f"Do you want to remove user '{member}' from '{selected_class_name}'?"
                            )
                            root.destroy()
                            if remove_answer:
                                # Find user by username
                                user_doc = db.users.find_one({"username": member})
                                if user_doc:
                                    db.classes.update_one(
                                        {"_id": ObjectId(selected_class_id)},
                                        {"$pull": {"members": user_doc["_id"]}}
                                    )
                                    db.users.update_one(
                                        {"_id": user_doc["_id"]},
                                        {"$pull": {"classes": ObjectId(selected_class_id)}}
                                    )
                                    classes_need_refresh = True
                                    remove_answer = None  # Reset answer after removal
            else:
                none_text = font2.render("none", True, (100, 100, 100))
                none_rect = none_text.get_rect(left=members_rect.left, top=members_display_y)
                screen.blit(none_text, none_rect)

        cross_img = pygame.image.load("./images/icons/cross.png")
        cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
        cross_rect = cross_img.get_rect(topright=(menu_rect.right - 10, menu_rect.top + 10))
        screen.blit(cross_img, cross_rect)

        if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
            # Reset all relevant state when menu closes
            
            input_active = False
            input_text = ""
            join_input_text = ""
            join_input_active = False
            addrepo_input_text = ""
            addrepo_input_active = False
            selected_class_id = None
            selectedrepo = None
            selected_file = None
            file_doc = None
            answer = None
            member_class_answer = None
            file_delete_answer = None
            repo_delete_answer = None
            remove_answer = None
            selected_class_name = "(select a class)"
            open_enabled = False
            classes_need_refresh = True
            panel_open = False

        upload_enabled = True if selected_class_role == "member" else False
        upload_btn_color = BLUE if upload_enabled else LIGHT_GRAY
        upload_text = font2.render("Upload File", True, WHITE)
        addrepo_text = font2.render("add task", True, WHITE)
        join_text = font2.render("join", True, WHITE)
        open_text = font2.render("Open", True, WHITE)

      # Create Class Button
        
           
        # Add Repo Button

        # Upload File Button - aligned left with addrepo, below it
        addrepo_rect = pygame.Rect(0, 0, addrepo_text.get_width() + 10, addrepo_text.get_height() + 10)
        addrepo_rect.center = (menu_rect.left + 820, menu_rect.bottom - 80)
        
        uploadfile_rect = pygame.Rect(0, 0, upload_text.get_width() + 10, upload_text.get_height() + 10)
        if is_teacher:
            uploadfile_rect.left = addrepo_rect.left - 40
            uploadfile_rect.top = addrepo_rect.bottom + 10
        else:
            uploadfile_rect.left = addrepo_rect.left - 40
            uploadfile_rect.top = menu_rect.bottom - 95
        pygame.draw.rect(screen, upload_btn_color, uploadfile_rect, border_radius=5)
        screen.blit(upload_text, (uploadfile_rect.x + 5, uploadfile_rect.y + 5))


        # Open Button - 10px to the left of uploadfile, vertically aligned
        open_rect = pygame.Rect(0, 0, open_text.get_width() + 10, open_text.get_height() + 10)
        if is_teacher:
            open_rect.top = uploadfile_rect.top
            open_rect.right = uploadfile_rect.left - 10
        else:
            open_rect.top = uploadfile_rect.top
            open_rect.right = uploadfile_rect.left - 10

       
        open_btn_color = BLUE if open_enabled else LIGHT_GRAY
        pygame.draw.rect(screen, open_btn_color, open_rect, border_radius=5)
        screen.blit(open_text, (open_rect.x + 5, open_rect.y + 5))  
        # join Button
        join_rect = pygame.Rect(0, 0, join_text.get_width() + 10, join_text.get_height() + 10)
        join_rect.center = (menu_rect.left + 515, menu_rect.bottom - 80)


        


        
        


        


        
       
        
        screen.blit(join_text, (join_rect.x + 5, join_rect.y + 5))
       
       

        # join button logic

        join_btn_color = BLUE
        upload_btn_color = BLUE if upload_enabled else LIGHT_GRAY
        # join input field
        join_input_box = pygame.Rect(0, 0, 120, 30)
        join_input_box.top = join_rect.top
        join_input_box.right = join_rect.left - 10

        # Draw join input box
        pygame.draw.rect(screen, WHITE, join_input_box)
        join_border_color = BLUE if join_input_active else WHITE
        pygame.draw.rect(screen, join_border_color, join_input_box, width=2)
        join_input_surface = font2.render(join_input_text, True, (0, 0, 0))
        screen.blit(join_input_surface, (join_input_box.x + 5, join_input_box.y + 5))

        # Draw join button (overwrite previous)
        pygame.draw.rect(screen, join_btn_color, join_rect, border_radius=5)
        screen.blit(join_text, (join_rect.x + 5, join_rect.y + 5))
    
        # Handle join input activation
        if join_input_box.collidepoint(mouse_pos) and left_mouse_button:
            join_input_active = True
            join_input_text = ""
        elif not join_input_box.collidepoint(mouse_pos) and left_mouse_button:
            join_input_active = False

        # Handle join input typing
        if join_input_active and event:
            if event.key == pygame.K_RETURN:
                join_input_active = False
            elif event.key == pygame.K_BACKSPACE:
                join_input_text = join_input_text[:-1]
            elif len(join_input_text) < 30:
                join_input_text += event.unicode

        # Handle join button click (by code, not invitation)
        if join_rect.collidepoint(mouse_pos) and left_mouse_button:
            if join_input_text.strip():
            # Find class by code
                class_doc = db.classes.find_one({"code": join_input_text.strip()})
            if class_doc:
                class_obj_id = class_doc["_id"]
                users_collection = db["users"]
                user_doc = users_collection.find_one({"username": username})
                if user_doc:
                    # Add user to class members
                    db["classes"].update_one(
                        {"_id": class_obj_id},
                        {"$addToSet": {"members": user_doc["_id"]}}
                    )
                    # Add class to user's classes array
                    users_collection.update_one(
                        {"_id": user_doc["_id"]},
                        {"$addToSet": {"classes": class_obj_id}}
                    )
                    classes_need_refresh = True  # Refresh class lists
                join_input_text = ""
                join_input_active = False
                # Reset join error timer if successful
               

        # Determine if selected class is taught by user

        # Add repo input box (to the left of addrepo button)
        if is_teacher:
            addrepo_input_box = pygame.Rect(0, 0, 120, 30)
            addrepo_input_box.top = addrepo_rect.top
            addrepo_input_box.right = addrepo_rect.left - 10

            pygame.draw.rect(screen, LIGHT_GRAY, addrepo_rect, border_radius=5)
            screen.blit(addrepo_text, (addrepo_rect.x + 5, addrepo_rect.y + 5))
            # Draw addrepo input box
            pygame.draw.rect(screen, WHITE, addrepo_input_box)
            addrepo_border_color = BLUE if addrepo_input_active else WHITE
            pygame.draw.rect(screen, addrepo_border_color, addrepo_input_box, width=2)
            addrepo_input_surface = font2.render(addrepo_input_text, True, (0, 0, 0))
            screen.blit(addrepo_input_surface, (addrepo_input_box.x + 5, addrepo_input_box.y + 5))

            # Draw addrepo button
            addrepo_btn_color = GREEN if selected_class_role == "teach" else LIGHT_GRAY
            pygame.draw.rect(screen, addrepo_btn_color, addrepo_rect, border_radius=5)
            screen.blit(addrepo_text, (addrepo_rect.x + 5, addrepo_rect.y + 5))

            # Handle addrepo input activation
            if addrepo_input_box.collidepoint(mouse_pos) and left_mouse_button and selected_class_role == "teach":
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
            if selected_class_role == "teach" and addrepo_rect.collidepoint(mouse_pos) and left_mouse_button:
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
        repo_table_x = repositories_in_rect.left - 65
        repo_table_y = repositories_in_rect.bottom + 40
        repo_rect_width = 120
        repo_rect_height = 30
        repo_margin_bottom = 10

        repo_rects = []
        for idx, repo_name in enumerate(repo_list):
            rect_y = repo_table_y + idx * (repo_rect_height + repo_margin_bottom)
            rect_color = (230, 230, 230) if idx % 2 == 0 else (255, 255, 255)
            # Highlight if selected
            if selectedrepo == repo_name:
                rect_color = BLUE
            repo_rect = pygame.Rect(repo_table_x, rect_y, repo_rect_width, repo_rect_height)
            repo_rects.append((repo_rect, repo_name))
            pygame.draw.rect(screen, rect_color, repo_rect)
            repo_name_color = WHITE if selectedrepo == repo_name else (0, 0, 0)
            repo_name_text = font2.render(repo_name, True, repo_name_color)
            screen.blit(repo_name_text, repo_name_text.get_rect(center=repo_rect.center))

            # Draw a cross icon 10px to the left of the repo rect
            if selected_class_role == "teach":
                repo_cross_img = pygame.image.load("./images/icons/cross.png")
                repo_cross_img = pygame.transform.smoothscale(repo_cross_img, (8, 8))
                repo_cross_x, repo_cross_y = repo_rect.topleft  # Unpack the tuple for topleft
                repo_cross_rect = repo_cross_img.get_rect(midright=(repo_cross_x, repo_cross_y))
                screen.blit(repo_cross_img, repo_cross_rect)

                # Handle cross click for deleting repo (only if user is teacher)
                if repo_cross_rect.collidepoint(mouse_pos) and left_mouse_button:
                    root = tk.Tk()
                    root.withdraw()
                    repo_delete_answer = messagebox.askyesno(
                        "Delete Repo",
                        f"Do you want to delete repo '{repo_name}'?"
                    )
                    root.destroy()
                    if repo_delete_answer:
                        # Remove repo from repositories list and repo_files dict
                        db.classes.update_one(
                        {"_id": ObjectId(selected_class_id)},
                        {
                            "$pull": {"repositories": repo_name},
                            "$unset": {f"repo_files.{repo_name}": ""}
                        }
                        )
                        # Refresh selected_class_doc so UI updates immediately
                        selectedrepo = None
                        selected_file = False
                        file_doc = None
                        selected_class_doc = db.classes.find_one({"_id": ObjectId(selected_class_id)})
                        repo_delete_answer = None  # Reset answer after deletion
            # --- Display files in this repo, 20px to the right, ONLY if selected ---
            if selectedrepo == repo_name:
                file_rects = []
                files = []
                if selected_class_doc and "repo_files" in selected_class_doc:
                    files = selected_class_doc["repo_files"].get(repo_name, [])
                    file_x = repo_rect.right + 20
                    file_y = repo_rect.y
                    file_rect_width = 120
                    file_rect_height = 25
                    file_margin_bottom = 5

                    for fidx, file_doc in enumerate(files):
                        file_rect_y = file_y + fidx * (file_rect_height + file_margin_bottom)
                        is_selected = selected_file == file_doc
                        # Correct color logic: green if seen_by_teacher, else blue if selected, else default
                        if file_doc.get("seen_by_teacher", False) and is_selected:
                            file_rect_color = BLUE
                        elif file_doc.get("seen_by_teacher", False):
                            file_rect_color = (0, 255, 0)
                        elif is_selected:
                            file_rect_color = BLUE
                        else:
                            file_rect_color = (245, 245, 245)
                        file_rect = pygame.Rect(file_x, file_rect_y, file_rect_width, file_rect_height)
                        file_rects.append((file_rect, file_doc))
                        pygame.draw.rect(screen, file_rect_color, file_rect)
                        file_name_color = WHITE if is_selected else (0, 0, 0)
                        file_name = file_doc.get("filename", "unnamed")
                        file_name_text = font2.render(file_name, True, file_name_color)
                        screen.blit(file_name_text, file_name_text.get_rect(center=file_rect.center))

                        # Only show cross icon if uploader is current user or user is teacher
                        if file_doc.get("uploader") == username or selected_class_role == "teach":
                            # Draw a cross icon 10px to the left of the file rect
                            file_cross_img = pygame.image.load("./images/icons/cross.png")
                            file_cross_img = pygame.transform.smoothscale(file_cross_img, (8, 8))
                            file_cross_x, file_cross_y = file_rect.topleft  # 10px left of file rect
                            file_cross_rect = file_cross_img.get_rect(midright=(file_cross_x, file_cross_y))
                            screen.blit(file_cross_img, file_cross_rect)

                            # Handle cross click for deleting file
                            if file_cross_rect.collidepoint(mouse_pos) and left_mouse_button:
                                root = tk.Tk()
                                root.withdraw()
                                file_delete_answer = messagebox.askyesno(
                                    "Delete File",
                                    f"Do you want to delete file '{file_name}'?"
                                )
                                root.destroy()
                                if file_delete_answer:
                                    # Remove file from repo_files.<repo_name> array
                                    db.classes.update_one(
                                        {"_id": ObjectId(selected_class_id)},
                                        {"$pull": {f"repo_files.{repo_name}": {"filename": file_name}}}
                                    )
                                    # Refresh selected_class_doc so UI updates immediately
                                    selected_file = False
                                    file_doc = None
                                    selected_class_doc = db.classes.find_one({"_id": ObjectId(selected_class_id)})
                                    file_delete_answer = None  # Reset answer after deletion
                        # Handle file selection
                        if left_mouse_button:
                            for file_rect, file_doc in file_rects:
                                if file_rect.collidepoint(mouse_pos):
                                    selected_file = file_doc


        # Handle repo selection
        if left_mouse_button:
            for repo_rect, repo_name in repo_rects:
                if repo_rect.collidepoint(mouse_pos):
                    selectedrepo = repo_name

        # --- Upload button logic ---
        upload_enabled = selectedrepo is not None  # Only enable if repo selected
        upload_btn_color = BLUE if upload_enabled else LIGHT_GRAY
        pygame.draw.rect(screen, upload_btn_color, uploadfile_rect, border_radius=5)
        screen.blit(upload_text, (uploadfile_rect.x + 5, uploadfile_rect.y + 5))

        # --- Open button logic ---
        if selected_file:
            open_enabled = True
        else:
            open_enabled = False
        
        pygame.draw.rect(screen, open_btn_color, open_rect, border_radius=5)
        screen.blit(open_text, (open_rect.x + 5, open_rect.y + 5))

        # Handle upload button click
        if upload_enabled and uploadfile_rect.collidepoint(mouse_pos) and left_mouse_button:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(title="Select Powerlink file", filetypes=[("Powerlink files", "*.pl"), ("All files", "*.*")])
            if file_path:
                if not file_path.lower().endswith(".pl"):
                    messagebox.showerror("Invalid file", "Please select a .pl (Powerlink) file.")
                else:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_data = f.read()
                        db.classes.update_one(
                            {"_id": ObjectId(selected_class_id), "repositories": selectedrepo},
                            {"$push": {f"repo_files.{selectedrepo}": {
                                "filename": username,
                                "data": file_data,  # Store as plain string, not JSON dump
                                "uploader": username,
                                "seen_by_teacher": False
                            }}},
                            upsert=True
                        )
                    messagebox.showinfo("Success", "File uploaded successfully!")
            root.destroy()
    
        # Handle open button click
        if open_enabled and open_rect.collidepoint(mouse_pos) and left_mouse_button:
            from functions.save_load_projects import load_mongo_file
            # selected_file is a dict with "data" as string
            file_name = selected_file.get("filename", "unnamed")
            # Now you have file_name and file_content
            file_content = selected_file.get("data", "")
            result = load_mongo_file(file_content, file_name)
            if isinstance(result, tuple) and len(result) == 2:
                comps, conns = result
                panel_open = False
            else:
                comps, conns = None, None
            # You should now use comps and conns as needed in your app


    return panel_open, comps, conns

def upload_feedback(mouse_pos, left_mouse_button, comps, cons):
    uploadfeedback_text = font2.render("save feedback", True, WHITE)
    upload_feedbackrect = uploadfeedback_text.get_rect(topleft=(1000, 12))
    screen.blit(uploadfeedback_text, upload_feedbackrect)

    if upload_feedbackrect.collidepoint(mouse_pos) and left_mouse_button:
        global selected_class_id, selectedrepo, selected_file

        # Check for missing repo, class id, or selected file
        if not selectedrepo or not selected_class_id or not selected_file:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", "currently not correcting student files! Select file in manage classes")
            root.destroy()
            return

        # Serialize feedback data (comps and cons) with UUID handling and class name
        from uuid import UUID

        serialized_comps = []
        for comp in comps:
            comp_data = comp.__dict__.copy()
            # Convert UUID to string, if present
            if isinstance(comp_data.get('id'), UUID):
                comp_data['id'] = str(comp_data['id'])
            comp_data['class_name'] = comp.__class__.__name__  # Store the class name
            serialized_comps.append(comp_data)

        serialized_connections = []
        for con in cons:
            con_data = con.__dict__.copy()
            # Convert UUID to string, if present
            if isinstance(con_data.get('id'), UUID):
                con_data['id'] = str(con_data['id'])
            con_data['class_name'] = con.__class__.__name__  # Store the class name
            serialized_connections.append(con_data)

        project_data = [serialized_comps, serialized_connections]
        feedback_json = json.dumps(project_data, indent=4)
        filename = selected_file.get("filename")
        print(selected_class_id, selectedrepo, filename)
        try:
            # Update the data field and set seen_by_teacher to True
            db.classes.update_one(
                {"_id": ObjectId(selected_class_id)},
                {
                    "$set": {
                        f"repo_files.{selectedrepo}.$[file].data": feedback_json,
                        f"repo_files.{selectedrepo}.$[file].seen_by_teacher": True
                    }
                },
                array_filters=[{"file.filename": filename}]
                )
            # Show success message in Tkinter
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Success", f"Feedback for {filename} saved and uploaded to cloud!")
            root.destroy()
            classes_need_refresh = True
            selected_file = False  # Reset selected file after upload
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Failed to upload feedback: {e}")
            root.destroy()

