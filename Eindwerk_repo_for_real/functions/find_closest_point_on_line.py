def find_closest_point_on_line(mouse_pos, line):
    """
    Find the closest point on a line to the given mouse position.
    """
    x1, y1 = line.start_pos
    x2, y2 = line.end_pos
    px, py = mouse_pos
    
    # Handle vertical line
    if x1 == x2:
        closest_x = x1
        closest_y = max(min(py, max(y1, y2)), min(y1, y2))
    # Handle horizontal line
    elif y1 == y2:
        closest_x = max(min(px, max(x1, x2)), min(x1, x2))
        closest_y = y1
    else:
        return None  # Non-axis-aligned lines are ignored in this implementation
    
    return closest_x, closest_y