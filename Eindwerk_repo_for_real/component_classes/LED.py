from component_classes.Component import Component

class LED(Component):
    def __init__(self):
        super().__init__(image_path="./images/Led.png", size_x=60, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "D"
        self.properties = [
            ["Voltage", 0],            
        ]
