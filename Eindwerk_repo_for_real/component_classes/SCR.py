from main.global_constants import BLACK
from component_classes.Component import Component

class SCR(Component):
    def __init__(self):
        super().__init__(image_path="./images/SCR.png", size_x=60, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "Q"
        self.properties = [
            ["Forward blocking voltage", 0],
            ["Gate trigger current", 0],
            ["Holding current", 0]            
        ]
