def check_line_overlap(new_line_start, new_line_end, existing_lines):
    """
    Checks if the new_line overlaps with any line in existing_lines.
    :param new_line: Tuple ((x1, y1), (x2, y2)) representing the new line.
    :param existing_lines: List of tuples representing existing lines.
    :return: True if overlap is detected, otherwise False.
    """
    def is_overlapping_segment(start1, end1, start2, end2):
        # Check if two segments overlap for at least 20px
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        return overlap_end - overlap_start >= 20

    new_x1, new_y1 = new_line_start
    new_x2, new_y2 = new_line_end

    for line in existing_lines:
        ex_x1, ex_y1 = line.start_pos
        ex_x2, ex_y2 = line.end_pos

        # Check horizontal overlap
        if new_y1 == new_y2 == ex_y1 == ex_y2:  # Both lines are horizontal
            if is_overlapping_segment(min(new_x1, new_x2), max(new_x1, new_x2), min(ex_x1, ex_x2), max(ex_x1, ex_x2)):
                return True
        
        # Check vertical overlap
        if new_x1 == new_x2 == ex_x1 == ex_x2:  # Both lines are vertical
            if is_overlapping_segment(min(new_y1, new_y2), max(new_y1, new_y2), min(ex_y1, ex_y2), max(ex_y1, ex_y2)):
                return True

    return False