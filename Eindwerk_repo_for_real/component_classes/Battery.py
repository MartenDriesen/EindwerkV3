from component_classes.Component import Component

class Battery(Component):
    def __init__(self):
        super().__init__(image_path="./images/Battery.png", size_x=60, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "V"
        self.properties = [
            ["Voltage", 0],            
        ]