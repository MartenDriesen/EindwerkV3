from functions.find_closest_point_on_line import find_closest_point_on_line

def line_is_near_pin(pin_pos, line, threshold=5):
    """
    Check if the pin is near the given line.
    """
    closest_point = find_closest_point_on_line(pin_pos, line)
    if closest_point:
        dist = ((pin_pos[0] - closest_point[0]) ** 2 + (pin_pos[1] - closest_point[1]) ** 2) ** 0.5
        return dist <= threshold
    return False