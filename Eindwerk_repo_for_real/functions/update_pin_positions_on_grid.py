from functions.component_data_pins_and_hotzones import component_pinout_with_hotzones

def update_pin_positions_on_grid(component):
    """
    Update the pin positions (pos_pin1, pos_pin2, pos_pin3...) of the component
    based on its current position, rotation, and the pinout data.
    """
    component_name = type(component).__name__  # e.g., "Resistor"

       # Iterate over the dictionary keys (tuples)
    for key_tuple, pinout_data in component_pinout_with_hotzones.items():
        if component_name in key_tuple:
            component_data = pinout_data
            break

    # Get the pinout data for the current rotation of the component
    pinout = component_data.get(component.rotation, [])

    # Initialize the pin positions to None (in case there are fewer than 4 pins)
    component.pos_pin1 = None
    component.pos_pin2 = None
    component.pos_pin3 = None
    component.pos_pin4 = None
    component.pos_pin5 = None
    component.pos_pin6 = None

    # Update the positions based on the available pinout data
    if len(pinout) > 0:
        component.pos_pin1 = (
            component.x + pinout[0]["pin"][0],
            component.y + pinout[0]["pin"][1]
        )
    if len(pinout) > 1:
        component.pos_pin2 = (
            component.x + pinout[1]["pin"][0],
            component.y + pinout[1]["pin"][1]
        )
    if len(pinout) > 2:
        component.pos_pin3 = (
            component.x + pinout[2]["pin"][0],
            component.y + pinout[2]["pin"][1]
        )
    if len(pinout) > 3:
        component.pos_pin4 = (
            component.x + pinout[3]["pin"][0],
            component.y + pinout[3]["pin"][1]
        )    
    if len(pinout) > 4:
        component.pos_pin5 = (
            component.x + pinout[4]["pin"][0],
            component.y + pinout[4]["pin"][1]
        )  
    if len(pinout) > 5:
        component.pos_pin6 = (
            component.x + pinout[5]["pin"][0],
            component.y + pinout[5]["pin"][1]
        )  