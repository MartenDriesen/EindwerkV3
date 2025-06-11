from component_classes.Component import Component

class LDR(Component):
    def __init__(self):
        super().__init__(image_path="./images/LDR.png", size_x=80, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "R"
        self.properties = [
            ["R_Dark", 0],    
            ["R_Light", 0]        
        ]
