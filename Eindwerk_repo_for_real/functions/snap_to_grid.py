from main.global_constants import SPACING # Importing constants

def snap_to_grid(x, y):
    """Snap coordinates to the nearest grid point."""
    grid_x = round(x / SPACING) * SPACING
    grid_y = round(y / SPACING) * SPACING 
    return grid_x, grid_y

def snap_to_virtual_grid(x, y, zoom_factor):
    """Snap coordinates to the nearest grid point."""
    grid_x = round(x / (SPACING + zoom_factor)) * (SPACING + zoom_factor)
    grid_y = round(y / (SPACING + zoom_factor)) * (SPACING + zoom_factor)
    return grid_x, grid_y