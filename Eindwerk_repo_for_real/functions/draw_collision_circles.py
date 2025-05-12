import pygame
from main.global_constants import screen, BLACK, SPACING
from functions.line_is_near_line import line_is_near_line
from functions.line_is_near_pin import line_is_near_pin

def draw_collision_circles(components, connections, camera_x, camera_y, zoom_factor):
    """
    Check for collisions of pins with other pins, or start/end of lines with other lines' middles,
    and draw circles at those positions.
    """
    # Check for pin collisions with other pins
    for component in components:
        pins = [
        component.pos_pin1, component.pos_pin2, component.pos_pin3,
        component.pos_pin4, component.pos_pin5, component.pos_pin6
    ]
        for pin_pos in pins:
            if pin_pos:  # Ensure the pin position exists
                # Check pin-to-pin collisions with other components
                for other_component in components:
                    if other_component != component:  # Ensure it's not the same component
                        other_pins = [
                            other_component.pos_pin1, other_component.pos_pin2, other_component.pos_pin3,
                            other_component.pos_pin4, other_component.pos_pin5, other_component.pos_pin6
                        ]
                        for other_pin in other_pins:
                            if other_pin and pin_pos == other_pin:  # Check for collision
                                # Calculate the position to draw
                                pin_pos_to_draw = (
                                    ((pin_pos[0] / SPACING) * (SPACING + zoom_factor)) - camera_x,
                                    ((pin_pos[1] / SPACING) * (SPACING + zoom_factor)) - camera_y
                                )
                                pygame.draw.circle(screen, BLACK, pin_pos_to_draw, 5)  # Draw black circle on collision


                # Check pin-to-line collisions
                for line in connections:
                    if line_is_near_pin(pin_pos, line):
                        pin_pos_to_draw = ((pin_pos[0] / SPACING) * (SPACING + zoom_factor)) - camera_x, ((pin_pos[1] / SPACING) * (SPACING + zoom_factor)) - camera_y
                        pygame.draw.circle(screen, BLACK, pin_pos_to_draw, 5)  # Draw black circle on collision

    # Check for start/end collisions with middles of other lines
    for i, line1 in enumerate(connections):
        for j, line2 in enumerate(connections):
            if i != j:  # Avoid checking the same line against itself
                # Check if the endpoints of line1 and line2 collide
                endpoints1 = [line1.start_pos, line1.end_pos]  # Start and end points of line1
                endpoints2 = [line2.start_pos, line2.end_pos]  # Start and end points of line2
            
                for endpoint1 in endpoints1:
                    for endpoint2 in endpoints2:
                        if endpoint1 == endpoint2:  # If the endpoints match
                            collision_point = ((endpoint1[0] / SPACING) * (SPACING + zoom_factor)) - camera_x, ((endpoint1[1] / SPACING) * (SPACING + zoom_factor)) - camera_y
                            pygame.draw.circle(screen, BLACK, collision_point, 4)  # Draw black circle
                            break
            
                # Detect if the lines themselves are near each other
                collision_point = line_is_near_line(line1, line2)
                if collision_point:
                    collision_point_to_draw = ((collision_point[0] / SPACING) * (SPACING + zoom_factor)) - camera_x, ((collision_point[1] / SPACING) * (SPACING + zoom_factor)) - camera_y
                    pygame.draw.circle(screen, BLACK, collision_point_to_draw, 5)  # Draw black circle at collision
