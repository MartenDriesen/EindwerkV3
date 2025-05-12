from component_classes.Component import Component

class PNP_Transistor(Component):
    def __init__(self):
        super().__init__(image_path="./images/PNP_transistor.png", size_x=80, size_y=60)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "T"
        self.properties = [
            ["Voltage", 0],            
        ]