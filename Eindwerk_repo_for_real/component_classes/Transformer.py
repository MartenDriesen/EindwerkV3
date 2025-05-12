from component_classes.Component import Component

class Transformer(Component):
    def __init__(self):
        super().__init__(image_path="./images/Transformator.png", size_x=80, size_y=100)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
