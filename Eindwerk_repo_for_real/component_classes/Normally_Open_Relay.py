from component_classes.Component import Component

class Normally_Open_Relay(Component):
    def __init__(self):
        super().__init__(image_path="./images/Relay_open.png", size_x=100, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
