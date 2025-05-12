from component_classes.Component import Component

class MOSFET_N_Enhance(Component):
    def __init__(self):
        super().__init__(image_path="./images/MOSFET_N_channel_enhancement_type.png", size_x=80, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "T"
        self.properties = [
            ["Voltage", 0],            
        ]
