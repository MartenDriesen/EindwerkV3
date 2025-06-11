from component_classes.Component import Component

class Circuit_Breaker(Component):
    def __init__(self):
        super().__init__(image_path="./images/switches/Circuit_Breaker_On.png", size_x=40, size_y=120)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "S"
        self.properties = [
            ["Max current", 0],            
        ]
