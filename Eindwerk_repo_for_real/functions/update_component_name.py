def update_component_name(components, dragged_comp, var):
    # Define the mapping of specific components to generalized types
    component_groups = {
    "Resistor": ["Resistor", "Varistor", "Thermistor", "LDR", "Potentiometer"],
    "Capacitor": ["Capacitor", "Var_Capacitor", "Polar_Capacitor", "Var_Polar_Capacitor"],
    "Diode": ["Diode", "Schottky_Diode", "Zener_Diode", "LED", "Photo_Diode"],
    "Inductor": ["Inductor", "Var_Inductor"],
    "Power_Source": ["Battery", "DC_Voltage_Src", "AC_Voltage_Src", "Three_Phase_Power_Src"],
    "Transistor": [
        "NPN_Transistor", "PNP_Transistor", "MOSFET_N_Depl.", "MOSFET_N_Enhance.",
        "MOSFET_P_Depl.", "MOSFET_P_Enhance.", "JFET_N_Channel", "JFET_P_Channel",
        "IGBT_N_Channel", "IGBT_P_Channel"
    ],
    "Thyristor": ["SCR", "Triac"],
    "Motor": ["DC_Motor", "AC_Motor", "Three_Phase_Motor_Delta", "Three_Phase_Motor_Star"],
    "Meter": ["Volt_Meter", "Current_Meter", "Ohm_Meter", "Power_Meter"],
    "Fuse": ["Fuse"],
    "Switch": [
        "Normally_Open_Relay", "SPS_Open", "DPST_Open", "TPST_Open", "SPST", "DPST",
        "Teleruptor", "Three_Way_Switch", "Four_Way_Switch", "Staircase_Timer_Auto", "Circuit_Breaker"
    ],
    "Transformer": ["Transformer"],
    "Ground": ["Ground"]
}


    # Reverse the mapping for quick lookup of generalized types
    type_to_group = {item: group for group, items in component_groups.items() for item in items}

    # Initialize a dictionary to keep track of how many components we have seen for each generalized type
    type_counts = {group: 0 for group in component_groups}

    # Iterate through the components and assign sequential numbers within their group
    for comp in components:
        # Get the specific component type (e.g., 'Varistor', 'Capacitor')
        comp_type = type(comp).__name__
        
        # Look up the generalized type from the mapping (e.g., 'Resistor' for 'Varistor')
        generalized_type = type_to_group.get(comp_type, comp_type)  # Fallback to comp_type if no match
        
        # Increment the count for this generalized type group
        type_counts[generalized_type] += 1
        
        # Rename the component using the first letter of the generalized type + its number
        comp.name = f"{comp.name[0]}{type_counts[generalized_type]}"
