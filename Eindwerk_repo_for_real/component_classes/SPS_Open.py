from main.global_constants import BLACK
from component_classes.Component import Component

class SPS_Open(Component):
    def __init__(self):
        super().__init__(image_path="./images/switches/SPS_Open.png", size_x=60, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
