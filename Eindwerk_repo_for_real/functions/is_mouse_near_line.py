from functions.find_closest_point_on_line import find_closest_point_on_line

def is_mouse_near_line(virtual_mouse_pos, line, threshold=5):
    """
    Check if the mouse is near a given line within a threshold distance.
    """
    closest_point = find_closest_point_on_line(virtual_mouse_pos, line)
    if not closest_point:
        return False, None
    dist = ((virtual_mouse_pos[0] - closest_point[0]) ** 2 + (virtual_mouse_pos[1] - closest_point[1]) ** 2) ** 0.5
    return dist <= threshold, closest_point