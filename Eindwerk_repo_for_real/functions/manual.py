import os
import subprocess
import pygame

def open_manual(event):
    # Check for Ctrl+M
    if event:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m and (pygame.key.get_mods() & pygame.KMOD_CTRL):
            manual_path = os.path.abspath("./manual/manual.pdf")
            print("manual")
            if os.name == 'nt':  # Windows
                os.startfile(manual_path)