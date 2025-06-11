from component_classes.Component import Component

class Polar_Capacitor(Component):
    def __init__(self):
        super().__init__(image_path="./images/Polarized_capacitor.png", size_x=60, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "C"
        self.properties = [
            ["µF", 0],            
        ]