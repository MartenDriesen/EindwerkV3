from component_classes.Component import Component

class IGBT_N_Channel(Component):
    def __init__(self):
        super().__init__(image_path="./images/IGBT_N_channel.png", size_x=80, size_y=60)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "Q"
        self.properties = [
            ["Max blocking voltage", 0],
            ["Treshold voltage", 0],
            ["Max amps", 0]            
        ]
