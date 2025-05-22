from main.global_constants import WHITE, font2, screen, DARKBLUE, BLUE, font6
import pygame
from pymongo import MongoClient
from bson import ObjectId
from tkinter import messagebox
import tkinter as tk
import json

# Setup MongoDB connection (if not already in your project)
client = MongoClient("mongodb+srv://marten2:123@powerlink-cluster.crculel.mongodb.net/?retryWrites=true&w=majority&appName=Powerlink-cluster")
db = client["powerlink"]

def upload_feedback(mouse_pos, left_mouse_button, comps, cons, selected_class_id, selectedrepo, selected_file):
    uploadfeedback_text = font2.render("save feedback", True, WHITE)
    upload_feedbackrect = uploadfeedback_text.get_rect(topleft=(900, 15))
    screen.blit(uploadfeedback_text, upload_feedbackrect)

    if upload_feedbackrect.collidepoint(mouse_pos) and left_mouse_button:
        print(selected_class_id, selectedrepo, selected_file)
        # Check for missing repo, class id, or selected file
        if not selectedrepo or not selected_class_id or not selected_file:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", "No repository, class, or file selected!")
            root.destroy()
            return

        # Serialize feedback data (comps and cons)
        feedback_data = [ [comp.__dict__ for comp in comps], [con.__dict__ for con in cons] ]
        feedback_json = json.dumps(feedback_data, indent=4)
        filename = selected_file.get("filename")
        try:
            # Update the data field and set seen_by_teacher to True
            db.classes.update_one(
                {
                    "_id": ObjectId(selected_class_id),
                    "repositories": selectedrepo,
                    f"repo_files.{selectedrepo}.filename": filename
                },
                {
                    "$set": {
                        f"repo_files.{selectedrepo}.$.data": feedback_json,
                        f"repo_files.{selectedrepo}.$.seen_by_teacher": True
                    }
                }
            )
            # Show success message in Tkinter
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Success", "Feedback saved and uploaded to MongoDB!")
            root.destroy()
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"Failed to upload feedback: {e}")
            root.destroy()

