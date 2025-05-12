from component_classes.Component import Component

class Three_Phase_Motor_Star(Component):
    def __init__(self):
        super().__init__(image_path="./images/Three_Phase_Motor_Star.png", size_x=80, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.name = "S"
        self.properties = [
            ["Ohm", 0],       # Resistance in ohms
            ["Voltage", 2],   # Voltage in volts
            ["Amps", 0],       # Current in amps
            ["mapa", 0],
            ["patat", 0] 
        ]
