import os
import shutil
from pymongo import MongoClient

from main.global_constants import WHITE, font2, screen

# MongoDB setup
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
groups_collection = db["groups"]
users_collection = db["users"]

def clear_directory(path):
    """Remove all contents of a directory but not the directory itself."""
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

def sync_user_groups_button(username, mouse_pos, left_mouse_button):
    sync_text = font2.render("sync", True, WHITE)
    syncrect = sync_text.get_rect(topleft=(900, 50))
    screen.blit(sync_text, syncrect)

    if syncrect.collidepoint(mouse_pos) and left_mouse_button:
        # Ensure base directories exist
        os.makedirs("./groups/classes_by_me", exist_ok=True)
        os.makedirs("./groups/classes", exist_ok=True)

        # ❌ Clear out existing folders first
        clear_directory("./groups/classes_by_me")
        clear_directory("./groups/classes")

        # ✅ 1. Recreate owned group folders
        owner_groups = groups_collection.find({"owner": username})
        for group in owner_groups:
            folder_path = f"./groups/classes_by_me/{group['name']}"
            os.makedirs(folder_path)
            print(f"Created folder (owner): {folder_path}")

        # ✅ 2. Recreate member group folders
        user = users_collection.find_one({"username": username})
        if not user:
            print("❌ User not found.")
            return

        member_group_ids = user.get("groups", [])
        member_groups = groups_collection.find({"_id": {"$in": member_group_ids}})
        for group in member_groups:
            folder_path = f"./groups/classes/{group['name']}"
            os.makedirs(folder_path)


def sync_user_groups(username):
   
        # Ensure base directories exist
    os.makedirs("./groups/classes_by_me", exist_ok=True)
    os.makedirs("./groups/classes", exist_ok=True)

        # ❌ Clear out existing folders first
    clear_directory("./groups/classes_by_me")
    clear_directory("./groups/classes")

        # ✅ 1. Recreate owned group folders
    owner_groups = groups_collection.find({"owner": username})
    for group in owner_groups:
        folder_path = f"./groups/classes_by_me/{group['name']}"
        os.makedirs(folder_path)
        print(f"Created folder (owner): {folder_path}")

        # ✅ 2. Recreate member group folders
    user = users_collection.find_one({"username": username})
    if not user:
        print("❌ User not found.")
        return

    member_group_ids = user.get("groups", [])
    member_groups = groups_collection.find({"_id": {"$in": member_group_ids}})
    for group in member_groups:
        folder_path = f"./groups/classes/{group['name']}"
        os.makedirs(folder_path)


