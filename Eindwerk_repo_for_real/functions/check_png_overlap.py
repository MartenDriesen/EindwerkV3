import pygame

def check_png_overlap(new_line_start, new_line_end, components):
    """
    Checks if the new_line overlaps any component's bounding box, 
    adjusted by shrinking 1 pixel on each side.
    
    :param new_line: Tuple ((x1, y1), (x2, y2)) representing the new line.
    :param components: List of placed components.
    :return: True if overlap is detected, otherwise False.
    """
    for comp in components:
        # Adjust the rectangle by shrinking it by 1 pixel on all sides
        rect = pygame.Rect(comp.x, comp.y, comp.size_x, comp.size_y)
        adjusted_rect = rect.inflate(-2, -2)
        if adjusted_rect.clipline(new_line_start, new_line_end):
            return True
    return False