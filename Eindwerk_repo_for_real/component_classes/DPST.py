from component_classes.Component import Component

class DPST(Component):
    def __init__(self):
        super().__init__(image_path="./images/switches/DPST.png", size_x=60, size_y=100)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.pos_pin5 = None
        self.pos_pin6 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
