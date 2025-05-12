from component_classes.Component import Component

class JFET_P_Channel(Component):
    def __init__(self):
        super().__init__(image_path="./images/JFET_P_channel.png", size_x=80, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "T"
        self.properties = [
            ["Voltage", 0],            
        ]
