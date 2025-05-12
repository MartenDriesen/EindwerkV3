from component_classes.Component import Component
from main.global_constants import BLACK

class Resistor(Component):
    def __init__(self):
        super().__init__(image_path="./images/Resistor.png", size_x=80, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "R"
        self.properties = [
            ["Ohm", 0],            
        ]
