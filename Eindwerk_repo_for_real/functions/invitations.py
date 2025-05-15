import pygame
from main.global_constants import WHITE, font2, screen, DARKBLUE, BLUE
import os
from pymongo import MongoClient
import shutil
# MongoDB setup at the top
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
users_collection = db["users"]

# State variables for the invitation panel
input_text = ""
input_active = False
draw_invite_panel = False
message = ""
selected_group = ""
draw_invitations_panel = False
dropdown_open = False

# Additional state variable for input border color

def sendinvitation(mouse_pos, left_mouse_button, event, current_user):
    global draw_invite_panel, input_text, input_active, message, selected_group, dropdown_open

    invite_text = font2.render("send invite", True, WHITE)
    inviterect = invite_text.get_rect(topleft=(1000, 12))
    screen.blit(invite_text, inviterect)

    if inviterect.collidepoint(mouse_pos) and left_mouse_button:
        draw_invite_panel = True
        input_active = True
        input_text = ""
        message = ""
        selected_group = ""
        dropdown_open = False

    if draw_invite_panel:
        
        panel_rect = pygame.Rect(950, 100, 300, 220)
        pygame.draw.rect(screen, DARKBLUE, panel_rect, border_radius=5)

        # Label
        label_text = font2.render("Username:", True, WHITE)
        screen.blit(label_text, (970, 110))

        # Username input field
        input_rect = pygame.Rect(970, 140, 200, 30)
        pygame.draw.rect(screen, WHITE, input_rect, border_radius=5)
        border_color = BLUE if input_active else WHITE
        pygame.draw.rect(screen, border_color, input_rect, 2, border_radius=5)
        input_surface = font2.render(input_text, True, (0, 0, 0))
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        # Group dropdown label
        screen.blit(font2.render("Select group:", True, WHITE), (970, 180))

        # Dropdown
        dropdown_rect = pygame.Rect(970, 210, 200, 30)
        pygame.draw.rect(screen, WHITE, dropdown_rect, border_radius=5)
        selected_text = font2.render(selected_group or "Choose...", True, (0, 0, 0))
        screen.blit(selected_text, (dropdown_rect.x + 5, dropdown_rect.y + 5))

        # Dropdown toggle
        if dropdown_open:
            try:
                group_folders = os.listdir("./groups/classes_by_me")
                for i, group in enumerate(group_folders):
                    group_rect = pygame.Rect(970, 240 + (i * 30), 200, 30)
                    pygame.draw.rect(screen, WHITE, group_rect)
                    group_text = font2.render(group, True, (0, 0, 0))
                    screen.blit(group_text, (group_rect.x + 5, group_rect.y + 5))
                    if group_rect.collidepoint(mouse_pos) and left_mouse_button:
                        selected_group = group
                        dropdown_open = False
            except:
                pass

        if dropdown_rect.collidepoint(mouse_pos) and left_mouse_button:
            dropdown_open = not dropdown_open

        # Send button
        send_button = pygame.Rect(970, 250, 80, 30)
        pygame.draw.rect(screen, BLUE, send_button, border_radius=5)
        screen.blit(font2.render("Send", True, WHITE), (send_button.x + 15, send_button.y + 5))

        # Cross button
        cross_img = pygame.image.load("./images/icons/cross.png")
        cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
        cross_rect = cross_img.get_rect(topleft=(panel_rect.right - 30, panel_rect.top + 10))
        screen.blit(cross_img, cross_rect)

        # Message
        if message:
            screen.blit(font2.render(message, True, WHITE), (panel_rect.x + 10, panel_rect.bottom - 30))

        # Input typing
        if event and input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                if len(input_text) < 20:
                    input_text += event.unicode

        # Send clicked
        if send_button.collidepoint(mouse_pos) and left_mouse_button:
            username = input_text.strip()
            if not username or not selected_group:
                message = "Enter user & class"
            else:
                user = users_collection.find_one({"username": username})
                group_doc = db["groups"].find_one({"name": selected_group, "owner": current_user})

                if user and group_doc:
                    db["invitations"].insert_one({
                        "to": username,
                        "from": current_user,
                        "group": group_doc["_id"]  # store ObjectId, not name
                    })
                    message = "Invitation sent!"
                else:
                    message = "User or group not found"


        if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
            draw_invite_panel = False
            input_active = False

def invitations(mouse_pos, left_mouse_button, current_user):
    global draw_invitations_panel

    invitations_text = font2.render("class Invitations", True, WHITE)
    invitationsrect = invitations_text.get_rect(topleft=(1100, 12))
    screen.blit(invitations_text, invitationsrect)

    if invitationsrect.collidepoint(mouse_pos) and left_mouse_button:
        draw_invitations_panel = True

    if draw_invitations_panel:
        panel_rect = pygame.Rect(1150, 30, 250, 300)
        pygame.draw.rect(screen, DARKBLUE, panel_rect, border_radius=5)

        # Close (X) icon
        cross_img = pygame.image.load("./images/icons/cross.png")
        cross_img = pygame.transform.smoothscale(cross_img, (20, 20))
        cross_rect = cross_img.get_rect(topleft=(panel_rect.right - 25, panel_rect.top + 5))
        screen.blit(cross_img, cross_rect)

        if cross_rect.collidepoint(mouse_pos) and left_mouse_button:
            draw_invitations_panel = False
            return  # Stop drawing rest if panel is closed

        # Load and display invitations
        invitations = list(db["invitations"].find({"to": current_user}))[:5]
        for i, invite in enumerate(invitations):
            y = panel_rect.y + 30 + i * 60
            group_text = font2.render(f"{invite['from']} invited to", True, WHITE)

            # Get the group name from the groups collection
            group_doc = db["groups"].find_one({"_id": invite["group"]})
            group_name_str = group_doc["name"] if group_doc else "Unknown Group"

            class_text = font2.render(group_name_str, True, WHITE)

            screen.blit(group_text, (panel_rect.x + 10, y))
            screen.blit(class_text, (panel_rect.x + 10, y + 20))

            ok_rect = pygame.Rect(panel_rect.x + 10, y + 40, 40, 20)
            x_rect = pygame.Rect(panel_rect.x + 60, y + 40, 40, 20)
            pygame.draw.rect(screen, BLUE, ok_rect)
            pygame.draw.rect(screen, (200, 50, 50), x_rect)
            screen.blit(font2.render("OK", True, WHITE), (ok_rect.x + 5, ok_rect.y))
            screen.blit(font2.render("X", True, WHITE), (x_rect.x + 10, x_rect.y))

            if ok_rect.collidepoint(mouse_pos) and left_mouse_button:
                invitation_id = invite["_id"]  # invitation document's _id

                group_obj_id = invite["group"]  # this is the group's ObjectId or string ID

                # If your _id fields are ObjectId type, convert the group_obj_id
                from bson import ObjectId
                if isinstance(group_obj_id, str):
                    group_obj_id = ObjectId(group_obj_id)

                # Find the group document by _id
                group = db["groups"].find_one({"_id": group_obj_id})
                if group:
                    group_name = group["name"]
                    src = f"./groups/classes by me/{group_name}"
                    dst = f"./groups/classes/{group_name}"
                    if os.path.exists(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)

                    # Add group to user's groups array
                    db["users"].update_one(
                        {"username": current_user},
                        {"$addToSet": {"groups": group_obj_id}}
                    )

                    # Remove the invitation
                    db["invitations"].delete_one({"_id": invitation_id})


            if x_rect.collidepoint(mouse_pos) and left_mouse_button:
                db["invitations"].delete_one({"_id": invite["_id"]})
