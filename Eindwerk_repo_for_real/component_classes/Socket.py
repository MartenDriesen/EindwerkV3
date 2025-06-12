from component_classes.Component import Component

class Socket(Component):
    def __init__(self):
        super().__init__(image_path="./images/Socket.png", size_x=40, size_y=40)
        self.pos_pin1 = None
        self.name = "J"

