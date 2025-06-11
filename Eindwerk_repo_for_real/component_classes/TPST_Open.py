from component_classes.Component import Component

class TPST_Open(Component):
    def __init__(self):
        super().__init__(image_path="./images/switches/TPST_Open.png", size_x=60, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.pos_pin4 = None
        self.pos_pin5 = None
        self.pos_pin6 = None
        self.name = "S"
