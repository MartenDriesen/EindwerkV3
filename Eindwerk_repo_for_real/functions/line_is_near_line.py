from functions.find_closest_point_on_line import find_closest_point_on_line

def line_is_near_line(line1, line2, threshold=5):
    """
    Check if the start or end position of `line1` is near the middle of `line2`,
    excluding the endpoints of `line2`.
    """
    start1 = line1.start_pos
    end1 = line1.end_pos
    # Helper: Check if a point matches another point
    def is_at_endpoint(point, line):
        return point == line.start_pos or point == line.end_pos

    # Check start1 against line2
    if not is_at_endpoint(start1, line2):  # Exclude if start1 is at line2's endpoints
        closest_to_start1 = find_closest_point_on_line(start1, line2)
        dist_start1 = ((start1[0] - closest_to_start1[0]) ** 2 + (start1[1] - closest_to_start1[1]) ** 2) ** 0.5
        if dist_start1 <= threshold:
            return start1  # Return the point causing the "collision"

    # Check end1 against line2
    if not is_at_endpoint(end1, line2):  # Exclude if end1 is at line2's endpoints
        closest_to_end1 = find_closest_point_on_line(end1, line2)
        dist_end1 = ((end1[0] - closest_to_end1[0]) ** 2 + (end1[1] - closest_to_end1[1]) ** 2) ** 0.5
        if dist_end1 <= threshold:
            return end1  # Return the point causing the "collision"

    return None  # No collision   