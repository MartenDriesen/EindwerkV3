import pygame
import os
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from pymongo import MongoClient
from main.global_constants import WHITE, font2, screen

# Setup MongoDB connection
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]
groups_collection = db["groups"]

# Global state message
class_created_msg = ""

def create_class(mouse_pos, left_mouse_button, user):
    global class_created_msg

    # Draw "create class" text button
    class_text = font2.render("create class", True, WHITE)
    classrect = class_text.get_rect(topleft=(900, 12))
    screen.blit(class_text, classrect)

    # Handle button click
    if classrect.collidepoint(mouse_pos) and left_mouse_button:
        # Ask for class name using tkinter
        tk.Tk().withdraw()  # Hide main tkinter window
        class_name = simpledialog.askstring("Create Class", "Enter class name:")

        if class_name:
            class_name = class_name.strip()

            try:
                # Insert group in MongoDB (no folder creation)
                groups_collection.insert_one({
                    "name": class_name,
                    "owner": user
                })

                # Create directory for the new class
                folder_path = os.path.join("./groups/classes_by_me", class_name)
                os.makedirs(folder_path, exist_ok=True)

                class_created_msg = f"✅ Created class: {class_name}"
            except Exception as e:
                class_created_msg = f"❌ Error: {str(e)}"
        else:
            class_created_msg = "❌ No class name entered"