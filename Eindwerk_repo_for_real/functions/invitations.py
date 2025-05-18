import pygame
from main.global_constants import WHITE, font2, screen, DARKBLUE, BLUE
from pymongo import MongoClient

client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
users_collection = db["users"]

draw_invitations_panel = False
dropdown_open = False

def invitations(mouse_pos, left_mouse_button, current_user):
    global draw_invitations_panel

    invitations_text = font2.render("Invitations", True, WHITE)
    invitationsrect = invitations_text.get_rect(topleft=(1300, 12))
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

        # Load and display invites (from 'invites' collection)
        invites = list(db["invites"].find({"to": current_user}))[:5]
        for i, invite in enumerate(invites):
            y = panel_rect.y + 30 + i * 60
            group_text = font2.render(f"{invite['from']} invited you to", True, WHITE)

            # Get the class name from the classes collection
            class_doc = db["classes"].find_one({"_id": invite["class_id"]})
            class_name_str = class_doc["name"] if class_doc else "Unknown Class"

            class_text = font2.render(class_name_str, True, WHITE)

            screen.blit(group_text, (panel_rect.x + 10, y))
            screen.blit(class_text, (panel_rect.x + 10, y + 20))

            ok_rect = pygame.Rect(panel_rect.x + 10, y + 40, 40, 20)
            x_rect = pygame.Rect(panel_rect.x + 60, y + 40, 40, 20)
            pygame.draw.rect(screen, BLUE, ok_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 50, 50), x_rect, border_radius=5)
            screen.blit(font2.render("OK", True, WHITE), (ok_rect.x + 5, ok_rect.y))
            screen.blit(font2.render("X", True, WHITE), (x_rect.x + 10, x_rect.y))

            if ok_rect.collidepoint(mouse_pos) and left_mouse_button:
                invitation_id = invite["_id"]
                class_obj_id = invite["class_id"]

                user_doc = users_collection.find_one({"username": current_user})
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

                # Remove the invite
                db["invites"].delete_one({"_id": invitation_id})

            if x_rect.collidepoint(mouse_pos) and left_mouse_button:
                db["invites"].delete_one({"_id": invite["_id"]})
