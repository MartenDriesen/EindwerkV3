from component_classes.Component import Component

class Inductor(Component):
    def __init__(self):
        super().__init__(image_path="./images/Inductor.png", size_x=100, size_y=40)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "L"
        self.properties = [
            ["Inductance", 0],            
        ]
