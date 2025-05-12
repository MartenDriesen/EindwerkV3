from component_classes.Component import Component

class Three_Phase_Power_Src(Component):
    def __init__(self):
        super().__init__(image_path="./images/Three_Phase_Power_Src.png", size_x=80, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.name = "V"
        self.properties = [
            ["Voltage", 0],            
        ]
