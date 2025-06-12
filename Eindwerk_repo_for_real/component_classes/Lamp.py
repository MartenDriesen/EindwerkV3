from component_classes.Component import Component

class Lamp(Component):
    def __init__(self):
        super().__init__(image_path="./images/Lamp.png", size_x=40, size_y=80)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.name = "L"