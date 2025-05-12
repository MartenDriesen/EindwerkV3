from main.global_constants import BLACK
from component_classes.Component import Component

class Staircase_Timer_Auto(Component):
    def __init__(self):
        super().__init__(image_path="./images/switches/Staircase_Timer_Auto.png", size_x=60, size_y=120)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
