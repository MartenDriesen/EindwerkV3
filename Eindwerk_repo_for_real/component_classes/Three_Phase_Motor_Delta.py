from component_classes.Component import Component

class Three_Phase_Motor_Delta(Component):
    def __init__(self):
        super().__init__(image_path="./images/Three_Phase_Motor_Delta.png", size_x=80, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "S"
        self.properties = [
            ["Voltage", 0],            
        ]
