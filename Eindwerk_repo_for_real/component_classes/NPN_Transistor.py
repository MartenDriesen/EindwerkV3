from component_classes.Component import Component

class NPN_Transistor(Component):
    def __init__(self):
        super().__init__(image_path="./images/NPN_transistor.png", size_x=80, size_y=60)
        self.pos_pin1 = None
        self.pos_pin2 = None
        self.pos_pin3 = None
        self.name = "Q"
        self.properties = [
            ["Max collector-emitter voltage", 0],
            ["Current gain", 0],
            ["Saturation voltage", 0],
            ["Base-emitter turn-on voltage", 0],
            ["Transition frequency", 0],
            ["Max collector current", 0]         
        ]
